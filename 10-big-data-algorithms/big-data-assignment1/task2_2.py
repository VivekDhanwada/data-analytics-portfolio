from mrjob.job import MRJob

class MRUserTotalSpending(MRJob):

    def mapper(self, _, line):
        try:
            line = line.strip().strip("{}").replace("'", "")
            user = ""
            money = 0.0
            for part in line.split(','):
                part = part.strip()
                if part.startswith("user_id"):
                    user = part.split(":")[1].strip()
                elif part.startswith("money"):
                    money = float(part.split(":")[1].strip())
            if user:
                yield user, money
        except:
            pass

    def reducer(self, key, values):
        yield key, round(sum(values), 2)

if __name__ == '__main__':
    MRUserTotalSpending.run()
