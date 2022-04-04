class User:
    def __init__(self, name, nickname, email):
        self.name = name
        self.nickname = nickname
        self.email = email

    def __str__(self):
        return f"{self.name} ({self.nickname}): {self.email}"
