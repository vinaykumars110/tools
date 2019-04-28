import xlrd

workbook = xlrd.open_workbook('hfcr_signas.xlsx')

worksheet = workbook.sheet_by_name('Sheet1')

#print(worksheet.cell(2, 3).value)
#print(int(worksheet.cell(2, 3).value))


for row in range(2,825):
    sig = worksheet.cell(row, 1).value
    dir = worksheet.cell(row, 2).value
    width = worksheet.cell(row, 3).value
    if type(width) == float:
        width = int(width)
    mod = worksheet.cell(row, 4).value
    desc = worksheet.cell(row, 5).value
    if sig != xlrd.empty_cell.value:
        if (type(width) == int) and (width > 1):
            #print(dir,'['+str(width-1)+':0]',sig, desc)
            print('{:10s} {:80s} {:35s} {}'.format(dir,'['+str(width-1)+':0]',sig+',', '// '+desc))
        elif (type(width) == int) and (width == 1):
            #print(dir, sig, desc)
            print('{:10s} {:80s} {:35s} {}'.format(dir, ' ', sig+',', '// '+desc))
        else:
            #print(dir, '[' + str(width) + '-1:0]', sig, desc)
            print('{:10s} {:80s} {:35s} {}'.format(dir, '[' + str(width) + '-1:0]', sig+',', '// '+desc))

'''
for row in range(2,825):
    sig = worksheet.cell(row, 1).value
    dir = worksheet.cell(row, 2).value
    width = worksheet.cell(row, 3).value
    if sig != xlrd.empty_cell.value:
        print(dir,sig)
'''