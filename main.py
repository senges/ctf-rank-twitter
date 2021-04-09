#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Author : @Pdrooo
# Version : Apr. 2021
# Description : Update Twitter bio with CTF score
# =============================================================================

from libs.RootMe import RootMe
from libs.TryHackMe import TryHackMe

import time
import twitter
import Settings

twitterAPI = twitter.Api(
    consumer_key        = Settings.TWITTER_CONSUMER_KEY,
    consumer_secret     = Settings.TWITTER_CONSUMER_SECRET,
    access_token_key    = Settings.TWITTER_TOKEN_KEY,
    access_token_secret = Settings.TWITTER_TOKEN_SECRET
)

# How long we should wait between
# every check

UPDATE_DELAY = 60

# Bio template

BIO_TEMPLATE = \
'''
Hello, this is my hacker bio !
Here are my challenge scores :
> {}
> {}

Take care
'''

# Update twitter user bio
def updateTwitterBio(bio: str):
    twitterAPI.UpdateProfile( description = bio )

# Entrypoint
def main():

    # New RootMe client
    rm = RootMe (
        Settings.ROOTME_LOGIN
    )

    # New TryHackMe client
    thm = TryHackMe (
        Settings.THM_LOGIN,
        Settings.THM_PASSWORD,
        Settings.THM_USERNAME
    )

    # Run forever
    while True:

        # If new informations
        if rm.update() or thm.update():
            
            # Twitter description
            bio  = BIO_TEMPLATE.format(
                rm.pprint(),    # Default class pretty print
                thm.pprint()    # Default class pretty print
            )

            # Update twitter bio
            updateTwitterBio( bio )

            print("Twitter bio updated")

        # Wait until next check
        time.sleep( UPDATE_DELAY )

if __name__ == "__main__":
    main()
