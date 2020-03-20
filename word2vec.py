import itertools
import json
import os
from gensim.models import KeyedVectors, Word2Vec
from gensim.models.fasttext import load_facebook_model
import numpy as np

def load_fastext_model(path):
	fb_model = load_facebook_model(path)
	return fb_model.wv


def gensim_from_vsmlib(path):
	#json_path = os.path.join(path, "meta_data.json")
	vector_path = os.path.join(path,"words100.npy")
	vocab_path = os.path.join(path,"words100.vocab")

	# with open(vocab_path,encoding='latin') as file:
	# 	meta_data = json.load(file)

	vectors = np.load(vector_path)

	vocab = list(line.rstrip('\n').split()[0] for line in open(vocab_path,'r',encoding='utf-8'))


	kv = KeyedVectors(100)
	kv.add(vocab, vectors)

	return kv


def load_word2vec_format(path):
	kv =  KeyedVectors.load_word2vec_format(path,binary=False,unicode_errors='replace')
	return kv

# def find_similar_groups(group,possible_words,top_n,threshhold):
#
# 	sim = [(wv.similarity(group, w), w) for w in possible_words]
# 	sim = sorted(sim, key=lambda v: v[0],)
#
# 	if possible_words and sim[0][0] > threshhold:
# 		return find_similar_groups([s[1] for s in sim[top_n:]],possible_words,top_n,threshhold)
# 	else:
# 		return sim[top_n:]

# def merge_similar_groups(wv,sim, top_n,threshhold):
# 	scors,words_tup = [zip(*sim)]
# 	best_n = sim[:top_n]
# 	res = []
# 	for t in words_tup:
# 		similars = [(s,t) for s in sim if s.intersection(t)]
#
# 		new_score = wv.similarity(group, w)

def remove_return(element, list):
  list.remove(element)
  return list

def find_similar_groups(wv,possible_words,threshhold):
	# tuples = [list(x) for x in itertools.combinations(possible_words, 2)]
	# sim = [(wv.similarity(t[0], t[1]), t) for t in tuples]
	# sim = sorted(sim, key=lambda v: v[0],)
	# groups = merge_similar_groups(sim,top_n)
	#
	# if possible_words and sim[0][0] > threshhold:
	# 	return find_similar_groups([s[1] for s in sim[top_n:]],possible_words,top_n,threshhold)
	# else:
	# 	return sim[top_n:]
	score = 0
	while(score<threshhold and len(possible_words) > 2):
		score = np.prod([wv.n_similarity(w,remove_return(w,list(possible_words))) for w in possible_words])
		remove_word = wv.doesnt_match(possible_words)
		possible_words.remove(remove_word)

	return possible_words

def similar_from_list(wv,words_def:str,possible_words,num):

	#normlize data
	#possible_words = possible_words.flatten()
	words_def = words_def.lower()
	possible_words = [w.lower() for w in possible_words]


	sim = np.sort([(wv.similarity(words_def,w.lower()), w) for w in possible_words])
	sim = sorted(sim,key=lambda v: v[0])
	print(sim)
	return [w for _,w in sim[-num:]]

def find_code_words(wv, positive, negative,threshhold=0.7,comb_n=4):
	positive = [p.lower() for p in positive]
	negative = []#[p.lower() for p in negative]
	groups = itertools.combinations(positive,comb_n)
	code_words = []
	score = 0
	for pos_group in groups:
		res = wv.most_similar(pos_group,negative,topn=1)
		code_words.append((res[0],pos_group))

	code_words = sorted(code_words,key=lambda t: t[0][1])
	return code_words[-1]

def create_similarity_matrix(wv,positive, negative):
	words = list(positive)+list(negative)
	len_pos,len_neg = len(positive) , len(negative)
	mat = np.zeros([len_pos,len_pos+len_neg])
	for i in range(len_pos):
		for j in range(len_pos+len_neg):
			mat[i,j] = wv.similarity(words[i],words[j])
			if(j>=len_pos):
				mat[i, j]*=-1
	return mat

def find_code_words_with_sim(wv, positive, negative,threshhold=0.7,comb_n=4):
	positive = [p.lower() for p in positive]
	negative = [p.lower() for p in negative]
	all_words_dict = positive+negative
	groups = itertools.combinations(positive, comb_n)
	code_words = []
	for pos_group in groups:
		similarityMatrix = create_similarity_matrix(wv, pos_group, negative)

		code_words.append((np.sum(similarityMatrix),pos_group))

	code_words = sorted(code_words,key=lambda t: t[0])
	words = code_words[-1]
	word = wv.most_similar(words[1])
	return (words,word)

if(__name__ == "__main__"):
	#filename = "data/word_linear_cbow_100d"
	gen_model = gensim_from_vsmlib("data/word_linear_cbow_100d")
	wv = gen_model.wv
	# similar_from_list(wv,'vampire', np.array([['WEREWOLF', 'CHAIN', 'MOSQUITO', 'CRAFT', 'RANCH'],
	#                                        ['LIP', 'VALENTINE', 'CLOUD', 'BEARD', 'BUNK'],
	#                                        ['SECOND', 'SADDLE', 'BUCKET', 'JAIL', 'BLOOD'],
	#                                        ['POCKET', 'LACE', 'BREAK', 'CUCKOO', 'FLAT'],
	#                                        ['BUFFY', 'CHERRY', 'CHRISTMAS', 'MOSES', 'TEAM']]), 3)



	#filename = "./data/cc.he.300.bin.gz"

	#wv = load_word2vec_format( "./data/model_heb.txt")

	#wv = gensim_from_vsmlib("./data/gold") #['דובדבן', 'כיס', 'שרוך']

	#wv = load_word2vec_format("./data/he.wiki.bpe.vs200000.d100.w2v.txt")

	#wv = gensim_from_vsmlib("./data/tweeter") #['דובדבן', 'כיס', 'שרוך']
	# similar_from_list(wv,'מתוק', np.array([['זאב', 'שרשרת', 'יתוש', 'מלאכה', 'חווה'],
	#                                        ['שפה', 'אהבה', 'ענן', 'זקן', 'גדה'],
	#                                        ['שניה', 'אוכף', 'דלי', 'כלא', 'דם'],
	#                                        ['כיס', 'שרוך', 'הפסקה', 'קוקיה', 'שטוח'],
	#                                        ['באפי', 'דובדבן', 'כריסטמס', 'משה', 'קבוצה']]), 3)

	# res = find_code_words(wv, ['ברוש', 'שרשרת', 'בנימין', 'באפי', 'דם',
	#                                         'עטלפים', 'אהבה', 'ענן', 'זקן', 'גדה'],negative=
	#                                         ['שניה', 'אוכף', 'דלי', 'כלא', 'דם',
	#                                         'כיס', 'שרוך', 'הפסקה', 'קוקיה', 'שטוח',
	#                                         'באפי', 'דובדבן', 'כריסטמס', 'משה', 'קבוצה'], top_n=30)

	res = find_code_words2(wv, positive=['WEREWOLF', 'CHAIN', 'MOSQUITO', 'CRAFT', 'RANCH',
	                              'LIP', 'VALENTINE', 'CLOUD', 'BEARD', 'BUNK',
	                              'BUFFY', 'SADDLE', 'BUCKET', 'JAIL', 'BLOOD'],
	                negative=['POCKET', 'LACE', 'BREAK', 'CUCKOO', 'FLAT',
	                          'BUFFY', 'CHERRY', 'CHRISTMAS', 'MOSES', 'TEAM'], top_n=3, threshhold=0.8)

	print(res)
	#print(wv.n_similarity(['זקן','זאב', 'בנימין'],['הרצל']))