"""
В модуле определены фунции для создания файлов
"""

__author__ = 'Dinmukhamed Stamaliev'

import io
import xlsxwriter
from service import get_min_value


def get_report_file(data):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)

    head_style = workbook.add_format(
        {
            'bold': True, 'border': 2, 'align': 'center',
        }
    )
    content_style = workbook.add_format(
        {
            'bold': False, 'border': 2, 'align': 'center',
        }
    )
    diff_style = workbook.add_format(
        {
            'bold': False, 'border': 0, 'align': 'center',
        }
    )
    worksheet = workbook.add_worksheet('report')

    columns = [
        'SKU',
        'model',
        'brand',
        'price',
        'PP1',
        'PP2',
        'PP3',
        'PP4',
        'PP5',
        'preorder',
    ]

    diff_columns = [
        'difference',
        'market name',
        'market price'
    ]

    for index, value in enumerate(columns):
        worksheet.write(0, index, value, head_style)

    for index, value in enumerate(diff_columns):
        worksheet.write(0, index+11, value, head_style)

    worksheet.set_column('A:A', 15)
    worksheet.set_column('B:B', 65)
    worksheet.set_column('C:C', 25)
    worksheet.set_column('D:J', 17)
    worksheet.set_column('L:L', 17)
    worksheet.set_column('M:M', 20)
    worksheet.set_column('N:N', 17)

    for i, tr in enumerate(data, start=1):
        data_dict = get_min_value(tr, tr['priceMin'])
        worksheet.write(i, 0, tr['sku'], content_style)
        worksheet.write(i, 1, tr['name'], content_style)
        worksheet.write(i, 2, tr['brand'], content_style)
        worksheet.write(i, 3,
                        tr['priceMin'] if tr['priceMin'] else tr['priceMax'],
                        content_style)
        worksheet.write(i, 4, 'yes', content_style)
        worksheet.write(i, 5, 'no', content_style)
        worksheet.write(i, 6, 'no', content_style)
        worksheet.write(i, 7, 'no', content_style)
        worksheet.write(i, 8, 'no', content_style)
        worksheet.write(i, 9, '', content_style)
        if data_dict:
            worksheet.write(i, 10, '', diff_style)
            worksheet.write(i, 11, data_dict['difference'], diff_style)
            worksheet.write(i, 12, data_dict['name'], diff_style)
            worksheet.write(i, 13, data_dict['price'], diff_style)

    workbook.close()
    return output.getvalue()
