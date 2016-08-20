#!/usr/bin/env python
# encoding: utf-8
#
# scaleThread.py
#
# Created by José Sánchez-Gallego on Aug 20, 2016.


from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import Queue

import guiderActor
from guiderActor import Msg, SCALE
import guiderActor.myGlobals

import opscore.utility.tback as tback


def apply_scale_offset(actor, guideCmd, offsetScale=None, tccOffsetFocus=None):
    """Commands the TCC to change scale or focus."""

    if offsetScale:
        cmdVar = actor.cmdr.call(actor='tcc', forUserCmd=guideCmd,
                                 cmdStr='set scale=%.9f /mult' % (offsetScale))
        if cmdVar.didFail:
            guideCmd.warn('text="Failed to issue scale change"')

    if tccOffsetFocus:
        cmdVar = actor.cmdr.call(actor='tcc', forUserCmd=guideCmd,
                                 cmdStr='set focus=%f/incremental' % (tccOffsetFocus),
                                 timeLim=20)
        if cmdVar.didFail:
            guideCmd.warn('text="Failed to issue focus offset"')

    return


def main(actor, queues):
    """Main for the scale/M2 offset thread."""

    threadName = 'scale'
    timeout = guiderActor.myGlobals.actorState.timeout

    while True:

        try:
            msg = queues[SCALE].get(timeout=timeout)
            qlen = queues[SCALE].qsize()

            if qlen > 0 and msg.cmd:
                msg.cmd.diag('scale thread has {0:d} items after a .get()'.format(qlen))

            if msg.type == Msg.EXIT:
                if msg.cmd:
                    msg.cmd.inform('text="Exiting thread {0}"'
                                   .format(threading.current_thread().name))
                return

            elif msg.type == Msg.SCALE_OFFSET:
                apply_scale_offset(actor, msg.cmd)

            else:
                raise ValueError('Unknown message type {0}'.format(msg.type))

        except Queue.Empty:
            actor.bcast.diag('text="guider movie alive"')

        except Exception as ee:
            actor.bcast.diag('text="movie thread got unexpected exception: {0}"'.format(ee))
            errMsg = 'Unexpected exception {0} in guider {1} thread'.format(ee, threadName)
            tback.tback(errMsg, ee)
