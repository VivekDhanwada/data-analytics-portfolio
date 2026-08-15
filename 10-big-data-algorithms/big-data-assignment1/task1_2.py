from mrjob.job import MRJob

class MRCoffeeSales(MRJob):

    def mapper(self, _, line):
        try:
            line = line.strip().strip('{}').replace("'", "")
            for part in line.split(','):
                part = part.strip()
                if part.startswith('coffee_type'):
                    coffee = part.split(':')[1].strip()
                elif part.startswith('money'):
                    money = float(part.split(':')[1].strip())
            yield coffee, money
        except:
            pass

    def reducer(self, key, values):
        yield key, round(sum(values), 2)

if __name__ == '__main__':
    MRCoffeeSales.run()
