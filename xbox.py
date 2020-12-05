import argparse
import asyncio
import os
from pprint import pprint
import sys
import wget
from tweet import TweetMachine
from moviepy.editor import *

from aiohttp import ClientResponseError, ClientSession

from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse
from xbox.webapi.scripts import CLIENT_ID, CLIENT_SECRET, TOKENS_FILE


async def async_main():
    parser = argparse.ArgumentParser(description="Change your gamertag")
    parser.add_argument(
        "--tokens",
        "-t",
        default=TOKENS_FILE,
        help=f"Token filepath. Default: '{TOKENS_FILE}'",
    )
    parser.add_argument(
        "--client-id",
        "-cid",
        default=os.environ.get("CLIENT_ID", CLIENT_ID),
        help="OAuth2 Client ID",
    )
    parser.add_argument(
        "--client-secret",
        "-cs",
        default=os.environ.get("CLIENT_SECRET", CLIENT_SECRET),
        help="OAuth2 Client Secret",
    )

    args = parser.parse_args()

    if not os.path.exists(args.tokens):
        print("No token file found, run xbox-authenticate")
        sys.exit(-1)

    async with ClientSession() as session:
        auth_mgr = AuthenticationManager(
            session, args.client_id, args.client_secret, ""
        )

        with open(args.tokens, mode="r") as f:
            tokens = f.read()
        auth_mgr.oauth = OAuth2TokenResponse.parse_raw(tokens)
        try:
            await auth_mgr.refresh_tokens()
        except ClientResponseError:
            print("Could not refresh tokens")
            sys.exit(-1)

        with open(args.tokens, mode="w") as f:
            f.write(auth_mgr.oauth.json())

        xbl_client = XboxLiveClient(auth_mgr)

        try:
            uniname = "c:/users/willr/downloads/UNIQUENAME8.mp4"
            resp = await xbl_client.gameclips.get_recent_own_clips(max_items=1)
            downloadLink = resp.game_clips[0].game_clip_uris[0].uri
            wget.download(downloadLink, uniname)
            clip = VideoFileClip(uniname).subclip(8)
            clip.write_videofile("c:/users/willr/downloads/UNIQUENAME8-finished.mp4",temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")
            clip.close()
            highlightz = TweetMachine()
            highlightz.makeAVidTweet('c:/users/willr/downloads/UNIQUENAME8-finished.mp4','🚨🚨🚨BUZZER BEATER ALERT🚨🚨🚨')
        except ClientResponseError:
            print("Invalid HTTP response")
            sys.exit(-1)

        pprint(resp.dict())


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())


if __name__ == "__main__":
    main()