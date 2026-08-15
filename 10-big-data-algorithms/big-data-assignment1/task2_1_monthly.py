from mrjob.job import MRJob

class MRMonthlySales(MRJob):
    def mapper(self, _, line):
        try:
            line = line.strip().strip("{}").replace("'", "")
            fields = line.split(",")
            coffee = ""
            money = 0.0
            month = ""

            for field in fields:
                key_val = field.strip().split(":")
                if len(key_val) == 2:
                    key, val = key_val[0].strip(), key_val[1].strip()
                    if key == "coffee_type":
                        coffee = val
                    elif key == "money":
                        money = float(val)
                    elif key == "month":
                        month = val

            if coffee and month:
                yield (coffee, month), money
        except:
            pass

    def reducer(self, key, values):
        yield list(key), round(sum(values), 2)

if __name__ == "__main__":
    MRMonthlySales.run()
