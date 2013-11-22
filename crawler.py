import sys
import datetime
sys.path.insert(0, '../../../../../Library/Python/2.6/site-packages')
import nltk
print 'import nltk complete'
print datetime.datetime.now()

from nltk.corpus import PlaintextCorpusReader
print 'plaintextcorpusreader complete'
print datetime.datetime.now()

corpus_root = '../../enron_mail_20110402'
enron = PlaintextCorpusReader(corpus_root, '.*')
print 'enron corpus root upload complete'
print datetime.datetime.now()

files = enron.fileids()
print 'fileids complete'
print datetime.datetime.now()

select_files = sorted([term for term in set(files) if 'sent' in term])
print 'selecting files from root complete'
print datetime.datetime.now()

csv_data = {}
count = 0
print count
months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

for file in select_files:
    if 'DS_Store' in file:
        continue
    else:
        email= '../../enron_mail_20110402/' + file
        fileHandle = open(email, 'r')
        read_lines = fileHandle.readlines()
        read_words = open(email, 'r').read()
            
        for line in read_lines:
            try:
                if line.startswith('X-FileName'):
                    length = len(line)
                if line.startswith('Date: Mon,') or line.startswith('Date: Tue,') or line.startswith('Date: Wed,') or line.startswith('Date: Thu,') or line.startswith('Date: Fri,') or line.startswith('Date: Sat,') or line.startswith('Date: Sun,'):
                    if ' ' in line[11:13]:
                        year = line[17:21]
                        month = line[13:16]
                        day = '0' + line[11:12]
                    else:
                        year = line[18:22]
                        month = line[14:17]
                        day = line[11:13]
                    
                    if months[month]:
                        num_month = months[month]
                        date = str(int(year + num_month + day))
                        print date
                        count = count + 1
                        print count
                    else:
                        continue
            except KeyError:
                print 'WARNING: Key Error Occurred'
                print datetime.datetime.now()
                continue
                
        begin = read_words.index('X-FileName')
            
        end_phrase = '-----Original Message-----'
            
        if end_phrase in read_words:
            end = read_words.index('-----Original Message-----')
        else:
            end = None
        
        body = read_words[(begin + length):end]
            
        from nltk.tokenize import word_tokenize, sent_tokenize
        body_token = [word for sent in sent_tokenize(body) for word in word_tokenize(sent)]
        filtered_body = filter(lambda word: word not in '.-' and word not in ',-' and word not in '?-' and word not in '!-' and word not in ';-' and word not in '$-' and word not in ')-' and word not in '(-' , body_token)
        total = float(len(filtered_body))
        if total == 0:
            total = 0.0000000001
            
        import sys
        sys.path.insert(0, '../../../../../Library/Python/2.6/site-packages')
        import nltk
        from nltk.corpus import PlaintextCorpusReader
        corpus_root = '../python'
        pos_words = PlaintextCorpusReader(corpus_root, 'positive_raw.txt')
        pos_wordlist = pos_words.words()
        similar = float(len([w for w in pos_wordlist if w in body]))
            
        if date not in csv_data:
            csv_data[date] = [similar, total, similar / total]
        else:
            temp_similar = 0
            temp_total = 0
            
            temp_list = csv_data[date]
            
            temp_similar = temp_list[0]
            temp_total = temp_list[1]
            
            csv_data[date] = [(similar + temp_similar), (total + temp_total), ((similar + temp_similar) / (total + temp_total))]
            
print 'nlp complete'
print datetime.datetime.now()
print 'initializing csv write'
print datetime.datetime.now()

for key in sorted(csv_data.iterkeys()):
    csv = open('positive_raw_20130731.csv', 'a')
    csv_data_temp = csv_data[key]
    csv.write("%s,%s\r\n" % (key, csv_data_temp[2]))
    csv.close()

print 'processing complete'
print datetime.datetime.now()
