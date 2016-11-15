from collections import defaultdict
import time
import bisect


class ThrottleBanner(object):
    def __init__(self, max_user_rps, ban_period):
        self.user_load = defaultdict(list)
        self.user_ban = set()
        self.user_last_access_time = defaultdict(int)
        self.max_user_rps = max_user_rps
        self.ban_period = ban_period

    def can_perform_request(self, user_id):
        current_time = int(time.time())
        is_banned = user_id in self.user_ban
        if is_banned and self.user_last_access_time[user_id] > current_time - self.ban_period:
            return False
        if is_banned:
            self.user_ban.remove(user_id)
        return self.update_ban(user_id, current_time)

    def update_ban(self, user_id, current_time):
        self.user_load[user_id].append(current_time)
        self.user_last_access_time[user_id] = current_time
        access_time_list = self.user_load[user_id]
        last_second_idx = bisect.bisect_left(access_time_list, current_time - 1)
        if last_second_idx:
            self.user_load[user_id] = access_time_list[last_second_idx:]
        if len(self.user_load[user_id]) > self.max_user_rps:
            self.user_ban.add(user_id)
            return False
        return True

