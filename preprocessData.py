write_handle = open('./company.txt', 'w', encoding='utf-8')

def preprocessData():
    with open('./jinrong.nt',encoding='UTF-8') as file:
        texts = file.read().splitlines()
        company_list = []
        for line in texts:
            line_list = line.split()
            company_list.append( line_list[0].split('/')[-1].split('>')[0] )
            company_list.append( line_list[2].split('/')[-1].split('>')[0] )
        company_set = set(company_list)
        for ii in company_set:
            write_handle.write( ii + ' ')
        write_handle.close()



if __name__ =='__main__':
    preprocessData()