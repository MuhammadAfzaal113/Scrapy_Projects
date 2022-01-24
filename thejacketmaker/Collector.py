import csv


def write_to_file(item, mode='a'):
    with open('leatherhidestore_Output.csv', mode=mode, encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')

        if mode == 'w':
            csv_writer.writerow(
                ['Product Name', 'Category', 'Sub-Category', 'Price', 'Competitor Price', 'Color', 'Size', 'Stock',
                 'Care', 'Texture', 'Finish',
                 'Feel', 'Quality', 'Notes', 'Important Note', 'Images', 'Project Images', 'Product URL']
            )

            print('file created as : leatherhidestore_Output.csv')
        else:
            csv_writer.writerow(
                [item.get('Product Name'), item.get('Category'), item.get('Sub-Category'), item.get('Price'),
                 item.get('Competitor Price'), item.get('Color'), item.get('Size'), item.get('Stock'), item.get('CARE'),
                 item.get('Texture'), item.get('Finish'), item.get('Feel'), item.get('Quality'), item.get('Notes'),
                 item.get('Important Note'), item.get('Images'), item.get('Project Images'), item.get('Product URL')
                 ]
            )
            print(item)


def get_urls_file(file_name, col):
    with open(file_name, 'r') as input_file:
        return [x[col] for x in csv.DictReader(input_file)]


if __name__ == '__main__':
    file_list = ['Outputs/output_24_01_2022_01_45_11.csv', 'Outputs/output_24_01_2022_01_49_23.csv',
                 'Outputs/output_24_01_2022_01_52_19.csv', 'Outputs/output_24_01_2022_01_55_02.csv',
                 'Outputs/output_24_01_2022_01_56_03.csv', 'Outputs/output_24_01_2022_01_56_52.csv',
                 'Outputs/output_24_01_2022_02_00_40.csv', 'Outputs/output_24_01_2022_02_03_30.csv',
                 'Outputs/output_24_01_2022_02_12_47.csv']
    write_to_file(item={}, mode='w')
    for file in file_list:
        prod_list = get_urls_file(file, 'Name')
        category_list = get_urls_file(file, 'Category')
        sub_list = get_urls_file(file, 'Sub-Category')
        price_list = get_urls_file(file, 'Price')
        comp_list = get_urls_file(file, 'Competitor Price')
        color_list = get_urls_file(file, 'Color')
        size_list = get_urls_file(file, 'Size')
        stock_list = get_urls_file(file, 'Stock')
        care_list = get_urls_file(file, 'CARE')
        tex_list = get_urls_file(file, 'Texture')
        finish_list = get_urls_file(file, 'Finish')
        feel_list = get_urls_file(file, 'Feel')
        quality_list = get_urls_file(file, 'Quality')
        notes_list = get_urls_file(file, 'Notes')
        imported_notes_list = get_urls_file(file, 'Important Note')
        image_list = get_urls_file(file, 'Images')
        project_list = get_urls_file(file, 'Project Images')
        prod_url_list = get_urls_file(file, 'Product URL')

        for index in range(len(prod_list)):
            if prod_list[index]:
                item = dict()
                item['Product Name'] = prod_list[index]
                item['Category'] = category_list[index]
                item['Sub-Category'] = sub_list[index]
                item['Price'] = price_list[index]
                item['Competitor Price'] = comp_list[index]
                item['Color'] = color_list[index]
                item['Size'] = size_list[index]
                item['Stock'] = stock_list[index]
                item['CARE'] = care_list[index]
                item['Texture'] = tex_list[index]
                item['Finish'] = finish_list[index]
                item['Feel'] = feel_list[index]
                item['Quality'] = quality_list[index]
                item['Notes'] = notes_list[index]
                item['Important Note'] = imported_notes_list[index]
                item['Images'] = image_list[index]
                item['Project Images'] = project_list[index]
                item['Product URL'] = prod_url_list[index]

                write_to_file(item=item)
