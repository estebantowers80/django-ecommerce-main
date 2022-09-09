import csv
from store.models import Category, Product

def load_categories():
    Category.objects.all().delete()
    with open('store/data/categorias.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')    
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column headers -> {"; ".join(row)}')
                line_count += 1
            else:
                print(f'Column values -> {"; ".join(row)}')            
                line_count += 1
                category = Category(name=row[0], slug=row[1])
                category.save()
                print(f'Category created: {category}')

        print(f'Processed {line_count} lines.')


def load_products():
    Product.objects.all().delete()
    with open('store/data/productos.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')    
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column headers -> {"; ".join(row)}')
                line_count += 1
            else:
                print(f'Column values -> {"; ".join(row)}')            
                line_count += 1
                product = Product(name=row[1],
                                  slug=row[2],
                                  description=row[3],
                                  image= 'images/' + row[4],
                                  price=row[5],
                                  is_active=row[6])
                product.save()
                category = Category.objects.get(slug= row[0])
                product.category.add(category)
                product.save()

        print(f'Processed {line_count} lines.')

def run():
    load_categories()
    load_products()