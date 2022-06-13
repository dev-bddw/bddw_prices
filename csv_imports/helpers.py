def return_updated_list(baseprice_record, this_record):
    new_price = int(baseprice_record[0][8]) + int(this_record[10])
    this_record[8] = new_price
    return this_record
