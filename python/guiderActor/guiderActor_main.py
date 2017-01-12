#!/usr/bin/env python
"""Start the guiderActor."""

import sys
from guiderActor import Msg, GuiderActor

# start a new actor
if __name__ == "__main__":
    location = None if len(sys.argv) == 1 else sys.argv[1]
    guider = GuiderActor.GuiderActor.newActor(location=location)
    guider.run(Msg=Msg)
