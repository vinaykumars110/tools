import xlrd
import re
import pprint
import sys

#ifile = sys.argv[1]
workbook = xlrd.open_workbook('ePAP_DWC_usb_address_map4.xlsx')
#workbook = xlrd.open_workbook(ifile)


worksheet = workbook.sheet_by_name('HCMDOUT')

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

# HCMDOUT registers parsing
worksheet_hco = workbook.sheet_by_name('HCMDOUT')
hco_cmds = []
for r in range(31, worksheet_hco.nrows):
    # print(r)
    if (worksheet_hco.cell(r, 1).value == 'Command') or (worksheet_hco.cell(r, 1).value == 'Command,no response'):
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
    if (worksheet_hci.cell(r, 1).value == 'Command') or (worksheet_hco.cell(r, 1).value == 'Command,no response'):
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


# CSR registers parsing
worksheet_csr = workbook.sheet_by_name('Local CSR')
csr_regs = []
for r in range(4, worksheet_csr.nrows):
    if worksheet_csr.cell(r,3).value == '':
        break
    reg_dict = {}
    reg_name = worksheet_csr.cell(r,1).value
    offset = str(worksheet_csr.cell(r, 2).value).split('x')[1]
    if (reg_name == '') or (reg_name == 'Reserved'):
        reg_name = 'reserved_' + offset
    reg_dict.update({'reg_name':reg_name})

    reg_dict.update({'offset':offset})
    type     = worksheet_csr.cell(r,3).value
    field    = worksheet_csr.cell(r,4).value
    if 'reserved_' in reg_name:
        field = "'0"
    reg_dict.update({'type':type})
    reg_dict.update({'field':field})
    fields_list = remove_text_inside_brackets(re.sub('[{}]', '', field)).split(',')
    fields_list = [x.strip(' ') for x in fields_list]
    fields_dict_list = []
    for cmd_par in fields_list:
        par_dict = {}
        if (cmd_par == 'Reserved') or (cmd_par == ''):
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
            width_format = '[31:0]'
            size = 32
            width_char_size = len(width_format)
        par_dict['signal_name'] = signal_name
        par_dict['width_format'] = width_format
        par_dict['size'] = size
        par_dict['width_char_size'] = width_char_size
        fields_dict_list.append(par_dict)
    reg_dict.update({'fields':fields_dict_list})
    reg_dict.update({'fmax_wchar_size': max(x['width_char_size'] for x in reg_dict['fields'])})
    if reg_dict != {}:
        if reg_dict['reg_name'] != '':
            csr_regs.append(reg_dict)


'''
# Debug purpose only
for cmd in hco_cmds:
    pprint.pprint(cmd)

for cmd in hci_cmds:
    pprint.pprint(cmd)
'''

for cmd in csr_regs:
    pprint.pprint(cmd)

# build data structure for each cmd
for cmd in hco_cmds:
    if cmd['cmd_pars'][0]['size'] != 0:
        #print('  //')
        print('  typedef struct packed {')
        s_name = 'hco_' + cmd['cmd_name'] + '_par_s'
        for p in cmd['cmd_pars']:
            print("    logic  " + p['width_format'] + " "*(cmd['cmdmax_wchar_size'] - len(p['width_format'])) + "  " + p['signal_name'] + ';')
        print('  } ' + s_name + ';')
        print('')

for cmd in hco_cmds:
    if cmd['sts_pars'][0]['size'] != 0:
        #print('  //')
        print('  typedef struct packed {')
        s_name = 'hco_' + cmd['cmd_name'] + '_stspar_s'
        for p in cmd['sts_pars']:
            print("    logic  " + p['width_format'] + " "*(cmd['cmdmax_wchar_size'] - len(p['width_format'])) + "  " + p['signal_name'] + ';')
        print('  } ' + s_name + ';')
        print('')

for cmd in hci_cmds:
    if cmd['cmd_pars'][0]['size'] != 0:
        #print('  //')
        print('  typedef struct packed {')
        s_name = 'hci_' + cmd['cmd_name'] + '_par_s'
        for p in cmd['cmd_pars']:
            print("    logic  " + p['width_format'] + " "*(cmd['cmdmax_wchar_size'] - len(p['width_format'])) + "  " + p['signal_name'] + ';')
        print('  } ' + s_name + ';')
        print('')

for cmd in hci_cmds:
    if cmd['sts_pars'][0]['size'] != 0:
        #print('  //')
        print('  typedef struct packed {')
        s_name = 'hci_' + cmd['cmd_name'] + '_stspar_s'
        for p in cmd['cmd_pars']:
            print("    logic  " + p['width_format'] + " "*(cmd['cmdmax_wchar_size'] - len(p['width_format'])) + "  " + p['signal_name'] + ';')
        print('  } ' + s_name + ';')
        print('')

#print('  //')
print('  function automatic [1:0] hcmdout_num_param_words (input hcmdout_cmd_type_e cmd_type, input mode);')
print('    logic [31:0] temp;')
print('    if (mode == 0) begin // CMD mode')
print('      case (cmd_type)')
flen = max(len(x['cmd_name']) for x in hco_cmds)
for cmd in hco_cmds:
    total_size = []
    for par in cmd['cmd_pars']:
        total_size.append(par['size'])
    total_size = '+'.join(map(str,total_size))
    print("        " + cmd['cmd_name'] + " " * (flen - len(cmd['cmd_name'])) + "  : temp = (" + total_size + ');')
print("        " + "default"       + " " * (flen - len('default'))       + "  : temp = (0);")
print('      endcase')
print('    end // CMD mode')
print('    else begin // STS mode')
print('      case (cmd_type)')
for cmd in hco_cmds:
    total_size = []
    for par in cmd['sts_pars']:
        total_size.append(par['size'])
    total_size = '+'.join(map(str,total_size))
    print("        " + cmd['cmd_name'] + " " * (flen - len(cmd['cmd_name'])) + "  : temp = (" + total_size + ');')
print("        " + "default" + " " * (flen - len('default')) + "  : temp = (0);")
print('      endcase')
print('    end // STS mode')
print("    return ((temp>128*3) ? 4 : (temp>128*2) ? 3 : (temp>128) ? 2 : (temp>0) ? 1 : 0);")
print('  endfunction // hcmdout_num_params')
print('')

#print('  //')
print('  function automatic [1:0] hcmdin_num_param_words (input hcmdin_cmd_type_e cmd_type, input mode);')
print('    logic [31:0] temp;')
print('    if (mode == 0) begin // CMD mode')
print('      case (cmd_type)')
flen = max(len(x['cmd_name']) for x in hci_cmds)
for cmd in hci_cmds:
    total_size = []
    for par in cmd['cmd_pars']:
        total_size.append(par['size'])
    total_size = '+'.join(map(str,total_size))
    print("        " + cmd['cmd_name'] + " " * (flen - len(cmd['cmd_name'])) + "  : temp = (" + total_size + ');')
print("        " + "default" + " " * (flen - len('default')) + "  : temp = (0);")
print('      endcase')
print('    end // CMD mode')
print('    else begin // STS mode')
print('      case (cmd_type)')
for cmd in hci_cmds:
    total_size = []
    for par in cmd['sts_pars']:
        total_size.append(par['size'])
    total_size = '+'.join(map(str,total_size))
    print("        " + cmd['cmd_name'] + " " * (flen - len(cmd['cmd_name'])) + "  : temp = (" + total_size + ');')
print("        " + "default" + " " * (flen - len('default')) + "  : temp = (0);")
print('      endcase')
print('    end // STS mode')
print("    return ((temp>128*3) ? 4 : (temp>128*2) ? 3 : (temp>128) ? 2 : (temp>0) ? 1 : 0);")
print('  endfunction // hcmdin_num_params')
print('')

#print('  //')
print('  function automatic hcmdout_cmd_is_valid (input hcmdout_cmd_type_e cmd_type);')
print('    logic temp;')
print('      case (cmd_type)')
flen = max(len(x['cmd_name']) for x in hco_cmds)
for cmd in hco_cmds:
    total_size = []
    for par in cmd['cmd_pars']:
        total_size.append(par['size'])
    total_size = '+'.join(map(str,total_size))
    print("        " + cmd['cmd_name'] + " " * (flen - len(cmd['cmd_name'])) + "  : temp = (1);")
print("        " + "default"       + " " * (flen - len('default'))       + "  : temp = (0);")
print('      endcase')
print("    return temp;")
print('  endfunction // hcmdout_cmd_is_valid')
print('')

#print('  //')
print('  function automatic hcmdin_cmd_is_valid (input hcmdin_cmd_type_e cmd_type);')
print('    logic temp;')
print('      case (cmd_type)')
flen = max(len(x['cmd_name']) for x in hci_cmds)
for cmd in hci_cmds:
    total_size = []
    for par in cmd['cmd_pars']:
        total_size.append(par['size'])
    total_size = '+'.join(map(str,total_size))
    print("        " + cmd['cmd_name'] + " " * (flen - len(cmd['cmd_name'])) + "  : temp = (1);")
print("        " + "default"       + " " * (flen - len('default'))       + "  : temp = (0);")
print('      endcase')
print("    return temp;")
print('  endfunction // hcmdin_cmd_is_valid')
print('')

# Local CSR Data structures
max_reg_name_char_size = max(len(x['reg_name']) for x in csr_regs)

for reg in csr_regs:
    if reg['type'] == 'RW':
        print("  reg [31:0] " + reg['reg_name'] + "_r;")

for reg in csr_regs:
    if reg['type'] == 'RW':
        print(reg['reg_name'] + "_r" + " "*(max_reg_name_char_size - len(reg['reg_name'])) + "   <= '0;")

for reg in csr_regs:

    if reg['type'] == 'R':
        print("  wire [31:0] " + reg['reg_name'] + "_rdata" + " "*(max_reg_name_char_size - len(reg['reg_name'])) + "   = " + reg['field'] + ";")
    elif reg['type'] == 'RW':
        print("  wire [31:0] " + reg['reg_name'] + "_rdata" + " "*(max_reg_name_char_size - len(reg['reg_name'])) + "   = " + reg['reg_name'] + "_r;")

regs=''
rev_csr_regs = list(reversed(csr_regs))
#print("  wire [31*" + str(len(csr_regs)) + "-1:0] csr_rdata = " + rev_csr_regs[0]['reg_name'] + "_rdata,")
print("  assign csr_rdata = {")
for reg in rev_csr_regs:
    regs += reg['reg_name'] + '_rdata, '
    print("                      /*"+reg['offset']+"*/  " +  reg['reg_name'] + "_rdata,")



for cmd in csr_regs:
    if ('reserved' or 'DWC_') not in cmd['reg_name']:
        #print('  //')
        print('  typedef struct packed {')
        s_name = 'csr_' + cmd['reg_name'] + '_s'
        for p in cmd['fields']:
            print("    logic  " + p['width_format'] + " "*(cmd['fmax_wchar_size'] - len(p['width_format'])) + "  " + p['signal_name'] + ';')
        print('  } ' + s_name + ';')
        print('')