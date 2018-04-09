# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright 2015-2018 by ExopyHqcLegacy Authors, see AUTHORS for more details.
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# -----------------------------------------------------------------------------
"""Tasks to set the parameters of arbitrary waveform generators.

"""
import logging

from atom.api import (Unicode, Enum, set_default)

from exopy.tasks.api import (InstrumentTask, validators)


class RunAWGTask(InstrumentTask):
    """ Task to set AWG run mode

    """
    #: Switch to choose the AWG run mode: on or off
    switch = Unicode('Off').tag(pref=True, feval=validators.SkipLoop())
    database_entries = set_default({'output': 0})
    mode = Enum('CONTINUOUS', 'TRIGGER', 'GATED','SEQUENCE').tag(pref=True)

    def perform(self, switch=None):
        """Default interface behavior.

        """
        self.driver.run_mode = self.mode        
        
        if switch is None:
            switch = self.format_and_eval_string(self.switch)

        running_state = self.driver.running

        if switch == 'On' or switch == 1:
            if running_state != '0 : Instrument has stopped':
                print('WARNING: AWG already running')
            for i in range(4):
                ch = self.driver.get_channel(i+1)
                if ch.channel_sequence:
                    ch.output_state = 'ON'
            self.driver.running = 1
            self.write_in_database('output', 1)
        else:
            self.driver.running = 0
            if running_state != '2 : Intrument is running':
                print('WARNING: AWG already stopped or waiting for a trigger')
            self.write_in_database('output', 0)
        log = logging.getLogger(__name__)
        msg = 'AWG running state OK'
        log.debug(msg)
