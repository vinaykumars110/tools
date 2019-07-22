import pprint

def search(d, search_pattern, prev_datapoint_path=''):
    output = []
    current_datapoint = d
    current_datapoint_path = prev_datapoint_path
    if type(current_datapoint) is dict:
        for dkey in current_datapoint:
            if search_pattern in str(dkey):
                c = current_datapoint_path
                c+="['"+dkey+"']"
                output.append(c)
            c = current_datapoint_path
            c+="['"+dkey+"']"
            for i in search(current_datapoint[dkey], search_pattern, c):
                output.append(i)
    elif type(current_datapoint) is list:
        for i in range(0, len(current_datapoint)):
            if search_pattern in str(i):
                c = current_datapoint_path
                c += "[" + str(i) + "]"
                output.append(i)
            c = current_datapoint_path
            c+="["+ str(i) +"]"
            for i in search(current_datapoint[i], search_pattern, c):
                output.append(i)
    elif search_pattern in str(current_datapoint):
        c = current_datapoint_path
        output.append(c)
    output = filter(None, output)
    return list(output)


if __name__ == "__main__":
    d = {'dict1':
             {'part1':
                  {'.wbxml': 'application/vnd.wap.wbxml',
                   '.rl': 'application/resource-lists+xml'},
              'part2':
                  {'.wsdl': 'application/wsdl+xml',
                   '.rs': 'application/rls-services+xml',
                   '.xop': 'application/xop+xml',
                   '.svg': 'image/svg+xml'}},
         'dict2':
             {'part1':
                  {'.dotx': 'application/vnd.openxmlformats-..',
                   '.zaz': 'application/vnd.zzazz.deck+xml',
                   '.xer': 'application/patch-ops-error+xml'}}}

    d2 = {
        "items":
            {
                "item":
                    [
                        {
                            "id": "0001",
                            "type": "donut",
                            "name": "Cake",
                            "ppu": 0.55,
                            "batters":
                                {
                                    "batter":
                                        [
                                            {"id": "1001", "type": "Regular"},
                                            {"id": "1002", "type": "Chocolate"},
                                            {"id": "1003", "type": "Blueberry"},
                                            {"id": "1004", "type": "Devil's Food"}
                                        ]
                                },
                            "topping":
                                [
                                    {"id": "5001", "type": "None"},
                                    {"id": "5002", "type": "Glazed"},
                                    {"id": "5005", "type": "Sugar"},
                                    {"id": "5007", "type": "Powdered Sugar"},
                                    {"id": "5006", "type": "Chocolate with Sprinkles"},
                                    {"id": "5003", "type": "Chocolate"},
                                    {"id": "5004", "type": "Maple"}
                                ]
                        },

                        ...

                    ]
            }
    }

    pprint.pprint(search(d,'svg+xml','d'))
    pprint.pprint(search(d2,'500','d2'))
    d3 = {"status":"success",
          "data":{
              "equity":{
                  "enabled":"true",
                  "net":11874.79,
                  "available":{"adhoc_margin":0,
                                 "cash":11874.79,
                                 "collateral":0,
                                 "intraday_payin":0},
                  "utilised":{"debits":0,
                                "exposure":0,
                                "m2m_realised":0,
                                "m2m_unrealised":0,
                                "option_premium":0,
                                "payout":0,
                                "span":0,
                                "holding_sales":0,
                                "turnover":0}},
              "commodity":{
                  "enabled":"true",
                  "net":0,
                  "available":{"adhoc_margin":0,
                                 "cash":0,
                                 "collateral":0,
                                 "intraday_payin":0},
                  "utilised":{"debits":0,
                               "exposure":0,
                               "m2m_realised":0,
                               "m2m_unrealised":0,
                               "option_premium":0,
                               "payout":0,
                               "span":0,
                               "holding_sales":0,
                               "turnover":0}}
          }
          }
    #d3 = #{"status": "success",

    d3 = {'a':'ab','c':[{'b':'ab'}]}
    #pprint.pprint(search(d2, 'id', 'd2'))
    #print(d3['data']['equity']['net'])
