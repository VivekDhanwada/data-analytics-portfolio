from mrjob.job import MRJob

class MRUserMonthlySpending(MRJob):

    def mapper(self, _, line):
        try:
            line = line.strip().strip("{}").replace("'", "")
            user = ""
            money = 0.0
            month = ""
            for part in line.split(','):
                part = part.strip()
                if part.startswith("user_id"):
                    user = part.split(":")[1].strip()
                elif part.startswith("money"):
                    money = float(part.split(":")[1].strip())
                elif part.startswith("month"):
                    month = part.split(":")[1].strip()
            if user and month:
                yield (user, month), money
        except:
            pass

    def reducer(self, key, values):
        yield list(key), round(sum(values), 2)

if __name__ == "__main__":
    MRUserMonthlySpending.run()
