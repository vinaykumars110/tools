import xlrd
import re
import pprint
import sys

ifile = sys.argv[1]
#workbook = xlrd.open_workbook('ePAP_DWC_usb_address_map.xlsx')
workbook = xlrd.open_workbook(ifile)


worksheet = workbook.sheet_by_name('HCMDOUT')

def search_cells(text):
    for r in range(0, worksheet.nrows):
        for c in range(0, worksheet.ncols):
            val = str(worksheet.cell(r, c).value)
            if text in val:
                print("CELL: " + str(r) + ' ' + str(c) + ' ' + str(val))


def search_cells_exact(text):
    result = False
    for r in range(0, worksheet.nrows):
        for c in range(0, worksheet.ncols):
            val = str(worksheet.cell(r, c).value)
            if text == val:
                print("CELL: " + str(r) + ' ' + str(c) + ' ' + str(val))
                result = True
    return result


# def remove_text_inside_brackets(text, brackets="()[]"):
def remove_text_inside_brackets(text, brackets="()"):
    count = [0] * (len(brackets) // 2)  # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b:  # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1) ** is_close  # `+1`: open, `-1`: close
                if count[kind] < 0:  # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else:  # character is not a [balanced] bracket
            if not any(count):  # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)


# search_cells_exact('Command')

# HCMDOUT registers parsing
worksheet_hco = workbook.sheet_by_name('HCMDOUT')
hco_cmds = []
for r in range(31, worksheet_hco.nrows):
    # print(r)
    if worksheet_hco.cell(r, 1).value == 'Command':
        # print(r)
        # Command Started here
        cmd_dict = {}
        for cr in range(r - 1, worksheet_hco.nrows):
            if cr == r - 1:
                cmd_name = remove_text_inside_brackets(worksheet_hco.cell(cr, 1).value).rstrip(' ')
                # print(cmd_name)
                cmd_dict.update({'cmd_name': cmd_name})
            if 'HCMDOUTPAR' in worksheet_hco.cell(cr, 1).value:
                cmd_pars_list = remove_text_inside_brackets(re.sub('[{}]', '', worksheet_hco.cell(cr, 2).value)).split(',')
                # remove spaces in signals
                cmd_pars_list = [x.strip(' ') for x in cmd_pars_list]
                # print(cmd_pars_list)
                par_dict_list = []
                for cmd_par in cmd_pars_list:
                    par_dict = {}
                    if 'NA' in cmd_par:
                        signal_name = 'NA'
                        width_format = ''
                        size = 0
                        width_char_size = 0
                    elif '[' in cmd_par:
                        signal_name = cmd_par.split('[')[0]
                        width_format = '[' + cmd_par.split('[')[1]
                        lx = cmd_par.split('[')[1].split(']')[0].split(':')[0]
                        rx = cmd_par.split('[')[1].split(']')[0].split(':')[1]
                        size = lx + '-' + rx + '+' + '1'
                        width_char_size = len(width_format)
                    else:
                        signal_name = cmd_par
                        width_format = ''
                        size = 1
                        width_char_size = len(width_format)
                    par_dict['signal_name'] = signal_name
                    par_dict['width_format'] = width_format
                    par_dict['size'] = size
                    par_dict['width_char_size'] = width_char_size
                    par_dict_list.append(par_dict)
                cmd_dict.update({'cmd_pars': par_dict_list})

            if 'HCMDOUTSTSPAR' in worksheet_hco.cell(cr, 1).value:
                cmd_pars_list = remove_text_inside_brackets(re.sub('[{}]', '', worksheet_hco.cell(cr, 2).value)).split(',')
                # remove spaces in signals
                cmd_pars_list = [x.strip(' ') for x in cmd_pars_list]
                # print(cmd_pars_list)
                par_dict_list = []
                for cmd_par in cmd_pars_list:
                    par_dict = {}
                    if 'NA' in cmd_par:
                        signal_name = 'NA'
                        width_format = ''
                        size = 0
                        width_char_size = 0
                    elif '[' in cmd_par:
                        signal_name = cmd_par.split('[')[0]
                        width_format = '[' + cmd_par.split('[')[1]
                        lx = cmd_par.split('[')[1].split(']')[0].split(':')[0]
                        rx = cmd_par.split('[')[1].split(']')[0].split(':')[1]
                        size = lx + '-' + rx + '+' + '1'
                        width_char_size = len(width_format)
                    else:
                        signal_name = cmd_par
                        width_format = ''
                        size = 1
                        width_char_size = len(width_format)
                    par_dict['signal_name'] = signal_name
                    par_dict['width_format'] = width_format
                    par_dict['size'] = size
                    par_dict['width_char_size'] = width_char_size
                    par_dict_list.append(par_dict)
                cmd_dict.update({'sts_pars': par_dict_list})
                break

            if (worksheet_hco.cell(cr, 1).value == 'Command') and (cr != r):
                break

        if 'sts_pars' not in cmd_dict:
            cmd_dict.update({'sts_pars':[{'signal_name':'NA',
                                          'size':0,
                                          'width_format':'',
                                          'width_char_size':0}]})
        cmd_dict.update({'cmdmax_wchar_size': max(x['width_char_size'] for x in cmd_dict['cmd_pars'])})
        cmd_dict.update({'stsmax_wchar_size': max(x['width_char_size'] for x in cmd_dict['sts_pars'])})
        hco_cmds.append(cmd_dict)





# HCMDIN registers parsing
worksheet_hci = workbook.sheet_by_name('HCMDIN')
hci_cmds = []
for r in range(14, worksheet_hci.nrows):
    # print(r)
    if worksheet_hci.cell(r, 1).value == 'Command':
        # print(r)
        # Command Started here
        cmd_dict = {}
        for cr in range(r - 1, worksheet_hci.nrows):
            if cr == r - 1:
                cmd_name = remove_text_inside_brackets(worksheet_hci.cell(cr, 1).value).rstrip(' ')
                # print(cmd_name)
                cmd_dict.update({'cmd_name': cmd_name})
            if 'HCMDINPAR' in worksheet_hci.cell(cr, 1).value:
                cmd_pars_list = remove_text_inside_brackets(re.sub('[{}]', '', worksheet_hci.cell(cr, 2).value)).split(',')
                # remove spaces in signals
                cmd_pars_list = [x.strip(' ') for x in cmd_pars_list]
                # print(cmd_pars_list)
                par_dict_list = []
                for cmd_par in cmd_pars_list:
                    par_dict = {}
                    if 'NA' in cmd_par:
                        signal_name = 'NA'
                        width_format = ''
                        size = 0
                        width_char_size = 0
                    elif '[' in cmd_par:
                        signal_name = cmd_par.split('[')[0]
                        width_format = '[' + cmd_par.split('[')[1]
                        lx = cmd_par.split('[')[1].split(']')[0].split(':')[0]
                        rx = cmd_par.split('[')[1].split(']')[0].split(':')[1]
                        size = lx + '-' + rx + '+' + '1'
                        width_char_size = len(width_format)
                    else:
                        signal_name = cmd_par
                        width_format = ''
                        size = 1
                        width_char_size = len(width_format)
                    par_dict['signal_name'] = signal_name
                    par_dict['width_format'] = width_format
                    par_dict['size'] = size
                    par_dict['width_char_size'] = width_char_size
                    par_dict_list.append(par_dict)
                cmd_dict.update({'cmd_pars': par_dict_list})

            if 'HCMDOUTPAR' in worksheet_hci.cell(cr, 1).value:
                cmd_pars_list = remove_text_inside_brackets(re.sub('[{}]', '', worksheet_hci.cell(cr, 2).value)).split(
                    ',')
                # remove spaces in signals
                cmd_pars_list = [x.strip(' ') for x in cmd_pars_list]
                # print(cmd_pars_list)
                par_dict_list = []
                for cmd_par in cmd_pars_list:
                    par_dict = {}
                    if 'NA' in cmd_par:
                        signal_name = 'NA'
                        width_format = ''
                        size = 0
                        width_char_size = 0
                    elif '[' in cmd_par:
                        signal_name = cmd_par.split('[')[0]
                        width_format = '[' + cmd_par.split('[')[1]
                        lx = cmd_par.split('[')[1].split(']')[0].split(':')[0]
                        rx = cmd_par.split('[')[1].split(']')[0].split(':')[1]
                        size = lx + '-' + rx + '+' + '1'
                        width_char_size = len(width_format)
                    else:
                        signal_name = cmd_par
                        width_format = ''
                        size = 1
                        width_char_size = len(width_format)
                    par_dict['signal_name'] = signal_name
                    par_dict['width_format'] = width_format
                    par_dict['size'] = size
                    par_dict['width_char_size'] = width_char_size
                    par_dict_list.append(par_dict)
                cmd_dict.update({'sts_pars': par_dict_list})
                break

            if (worksheet_hci.cell(cr, 1).value == 'Command') and (cr != r):
                break

        if 'sts_pars' not in cmd_dict:
            cmd_dict.update({'sts_pars':[{'signal_name':'NA',
                                          'size':0,
                                          'width_format':'',
                                          'width_char_size':0}]})
        cmd_dict.update({'cmdmax_wchar_size':max(x['width_char_size'] for x in cmd_dict['cmd_pars'])})
        cmd_dict.update({'stsmax_wchar_size': max(x['width_char_size'] for x in cmd_dict['sts_pars'])})
        hci_cmds.append(cmd_dict)

for cmd in hco_cmds:
    pprint.pprint(cmd)

for cmd in hci_cmds:
    pprint.pprint(cmd)

# build data structure for each cmd

for cmd in hco_cmds:
    if cmd['cmd_pars'][0]['size'] != 0:
        #print('//')
        print('typedef struct packed {')
        s_name = cmd['cmd_name'] + '_par_s'
        for p in cmd['cmd_pars']:
            print("  logic  " + p['width_format'] + " "*(cmd['cmdmax_wchar_size'] - len(p['width_format'])) + "  " + p['signal_name'] + ';')
        print('} ' + s_name + ';')
        print('')

for cmd in hci_cmds:
    if cmd['cmd_pars'][0]['size'] != 0:
        #print('//')
        print('typedef struct packed {')
        s_name = cmd['cmd_name'] + '_par_s'
        for p in cmd['cmd_pars']:
            print("  logic  " + p['width_format'] + " "*(cmd['cmdmax_wchar_size'] - len(p['width_format'])) + "  " + p['signal_name'] + ';')
        print('} ' + s_name + ';')
        print('')

#print('//')
print('function automatic [1:0] hcmdout_num_params (input hcmdout_cmd_type_e cmd_type);')
print('  logic [128:0] temp;')
print('  case (cmd_type)')
flen = max(len(x['cmd_name']) for x in hco_cmds)
for cmd in hco_cmds:
    total_size = []
    for par in cmd['cmd_pars']:
        total_size.append(par['size'])
    total_size = '+'.join(map(str,total_size))
    print("    " + cmd['cmd_name'] + " " * (flen - len(cmd['cmd_name'])) + "  : temp = (" + total_size + ');')
print('  endcase')
print('  return (temp[128+:128*3] ? 4 : temp[128+:128*2] ? 3 : temp[128+:128*1] ? 2 : temp[128+:0] ? 1 : 0);')
print('endfunction // hcmdout_num_params')
print('')

#print('//')
print('function automatic [1:0] hcmdin_num_params (input hcmdin_cmd_type_e cmd_type);')
print('  logic [128:0] temp;')
print('  case (cmd_type)')
flen = max(len(x['cmd_name']) for x in hco_cmds)
for cmd in hci_cmds:
    total_size = []
    for par in cmd['cmd_pars']:
        total_size.append(par['size'])
    total_size = '+'.join(map(str,total_size))
    print("    " + cmd['cmd_name'] + " " * (flen - len(cmd['cmd_name'])) + "  : temp = (" + total_size + ');')
print('  endcase')
print('  return (temp[128+:128*3] ? 4 : temp[128+:128*2] ? 3 : temp[128+:128*1] ? 2 : temp[128+:0] ? 1 : 0);')
print('endfunction // hcmdin_num_params')
print('')


