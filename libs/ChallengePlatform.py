import requests

class UserInfo:
    # Handle data as strings for more
    # convenience
    def __init__(self, rank: str, nrank: str, score: str, solves: list):
        self.rank = rank
        self.nrank = nrank
        self.score = score
        self.solves = solves    # Challenges solves not yet implemented

    # To make UserInfo obj comparable
    def __eq__(self, other: UserInfo): 
        return (
            self.rank == other.rank
            and self.nrank == other.nrank
            and self.score == other.score
            and self.solves == other.solves
        )

# Informal unified interface for
# challenges platform

class ChallengePlatform:
    def get(self, url: str) -> requests.Response:
        """Unified API or website get method"""
        pass

    def update(self) -> bool:
        """Update infos"""
        pass

    def fetchInfos(self) -> UserInfo:
        """Fetch user infos"""
        pass

    def yieldInfos(self) -> UserInfo:
        """Return user infos without refresh"""

    def pprint(self) -> str:
        """Pretty print user infos"""
        pass

    def panic(self, msg):
        """Program panic"""
        print(f'Error : {msg}')
        exit(1)