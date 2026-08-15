from mrjob.job import MRJob
from mrjob.step import MRStep

class MRCoffeeTotalSales(MRJob):

    def mapper_extract_coffee_sales(self, _, line):
        # Clean and parse the input line
        line = line.strip().strip('{}').replace("'", "")
        
        coffee = None
        money = 0.0
        
        for part in line.split(','):
            part = part.strip()
            if ':' not in part:
                continue
                
            key, value = part.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if key == 'coffee_type':
                coffee = value
            elif key == 'money':
                try:
                    money = float(value)
                except ValueError:
                    pass
        
        if coffee:
            yield coffee, money

    def reducer_sum_sales(self, coffee, amounts):
        total = round(sum(amounts), 2)
        # Emit (total, coffee) to sort by sales later
        yield None, (total, coffee)

    def reducer_sort_by_sales(self, _, sales_pairs):
        # Sort all (total, coffee) pairs by total (ascending)
        for total, coffee in sorted(sales_pairs):
            yield coffee, total

    def steps(self):
        return [
            MRStep(
                mapper=self.mapper_extract_coffee_sales,
                reducer=self.reducer_sum_sales
            ),
            MRStep(
                reducer=self.reducer_sort_by_sales
            )
        ]

if __name__ == '__main__':
    MRCoffeeTotalSales.run()