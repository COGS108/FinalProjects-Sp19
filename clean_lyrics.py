import re
import string

def clean_lyrics(lyrics):
    #Normalize case sensitive names before lowercasing them
    lyrics = lyrics.replace("Johnson", "president")
    lyrics = lyrics.replace("Trump", "president")

    lyrics = lyrics.lower()
    lyrics = lyrics.strip()
    lyrics = lyrics.replace("can't", "can not")
    lyrics = lyrics.replace("won't", "will not")
    lyrics = lyrics.replace("ain't", "aint")
    lyrics = lyrics.replace("n't", " not")
    lyrics = lyrics.replace("'ll", " will")
    lyrics = lyrics.replace("'re", " are")
    lyrics = lyrics.replace("'ve", " have")
    lyrics = lyrics.replace("'m", " am")
    lyrics = lyrics.replace("how'd", "how did")
    lyrics = lyrics.replace("'d", " would")
    lyrics = lyrics.replace("it's", "it is")
    lyrics = lyrics.replace("'til", "until")
    lyrics = lyrics.replace("'s", "s")
    lyrics = lyrics.replace("in'", "ing")
    lyrics = lyrics.replace("'cause", "because")
    lyrics = lyrics.replace("gon'", "going to")
    lyrics = lyrics.replace("gonna", "going to")
    lyrics = lyrics.replace("'bout", "about")
    lyrics = lyrics.replace("y'all", "you all")
    lyrics = lyrics.replace("tryna'", "trying to")
    lyrics = lyrics.replace("lil'", "little")
    lyrics = lyrics.replace("'em", "them")
    lyrics = lyrics.replace("'im", "him")
    lyrics = re.sub("[\[].*?[\]]", "", lyrics)
    lyrics = lyrics.translate(str.maketrans('', '', string.punctuation))
    lyrics = lyrics.replace(" ya ", " you ")

    # Normalizing terms for `gun`
    lyrics = lyrics.replace("bullet", "gun")
    lyrics = lyrics.replace("guns", "gun")
    lyrics = lyrics.replace("aa-12", "gun")
    lyrics = lyrics.replace("ak-47", "gun")
    lyrics = lyrics.replace("ak-5", "gun")
    lyrics = lyrics.replace("ak-74", "gun")
    lyrics = lyrics.replace("ar-15", "gun")
    lyrics = lyrics.replace("calico", "gun")
    lyrics = lyrics.replace("caliber", "gun")
    lyrics = lyrics.replace("desert eagle", "gun")
    lyrics = lyrics.replace("draco", "gun")
    lyrics = lyrics.replace("famas", "gun")
    lyrics = lyrics.replace("five-seven", "gun")
    lyrics = lyrics.replace("five seven", "gun")
    lyrics = lyrics.replace("p90", "gun")
    lyrics = lyrics.replace("glock", "gun")
    lyrics = lyrics.replace("luger", "gun")
    lyrics = lyrics.replace("m16", "gun")
    lyrics = lyrics.replace("m1", "gun")
    lyrics = lyrics.replace("m21", "gun")
    lyrics = lyrics.replace("m4", "gun")
    lyrics = lyrics.replace("m9", "gun")
    lyrics = lyrics.replace("mac-10", "gun")
    lyrics = lyrics.replace("mac-11", "gun")
    lyrics = lyrics.replace("mac-12", "gun")
    lyrics = lyrics.replace("master key", "gun")
    lyrics = lyrics.replace("ruger", "gun")
    lyrics = lyrics.replace("blackhawk", "gun")
    lyrics = lyrics.replace("sks", "gun")
    lyrics = lyrics.replace("tec-9", "gun")
    lyrics = lyrics.replace("uzi", "gun")
    lyrics = lyrics.replace("colt", "gun")
    lyrics = lyrics.replace("armalite", "gun")
    lyrics = lyrics.replace("beretta", "gun")
    lyrics = lyrics.replace("glock", "gun")
    lyrics = lyrics.replace("heckler & koch", "gun")
    lyrics = lyrics.replace("kel-tec", "gun")
    lyrics = lyrics.replace("intratec", "gun")
    lyrics = lyrics.replace("mossberg", "gun")
    lyrics = lyrics.replace("ruger", "gun")
    lyrics = lyrics.replace("sig", "gun")
    lyrics = lyrics.replace("taurus", "gun")
    lyrics = lyrics.replace("sinchester", "gun")
    lyrics = lyrics.replace("smith & wesson", "gun")
    lyrics = lyrics.replace("smith and wesson", "gun")
    lyrics = lyrics.replace("revolver", "gun")

    # Normalizing terms for `war`
    lyrics = lyrics.replace("combat", "war")
    lyrics = lyrics.replace("fighting", "war")
    lyrics = lyrics.replace("fightin'", "war")
    lyrics = lyrics.replace("battlefield", "war")
    lyrics = lyrics.replace("battle", "war")
    lyrics = lyrics.replace("warfare", "war")
    lyrics = lyrics.replace("war-worn", "war")
    lyrics = lyrics.replace("war-torn", "war")
    lyrics = lyrics.replace("bloodshed", "war")

    # Normalizing terms for `death`
    lyrics = lyrics.replace("die", "death")
    lyrics = lyrics.replace("dying", "death")
    lyrics = lyrics.replace("dead", "death")
    lyrics = lyrics.replace("kill", "death")
    lyrics = lyrics.replace("killed", "death")
    lyrics = lyrics.replace

    # Normalizing terms for `soldiers`
    lyrics = lyrics.replace("soldier", "soldiers")
    lyrics = lyrics.replace("private", "soldiers")
    lyrics = lyrics.replace("trooper", "soldiers")
    lyrics = lyrics.replace("troops", "soldiers")
    lyrics = lyrics.replace("army", "soldiers")
    lyrics = lyrics.replace("military", "soldiers")
    lyrics = lyrics.replace("navy", "soldiers")
    lyrics = lyrics.replace("veteran", "soldiers")
    lyrics = lyrics.replace("veterans", "soldiers")
    lyrics = lyrics.replace("vet", "soldiers")
    lyrics = lyrics.replace("vets", "soldiers")

    # Normalizing terms for `protest`
    lyrics = lyrics.replace("protesting", "protest")
    lyrics = lyrics.replace("protests", "protest")
    lyrics = lyrics.replace("picket line", "protest")
    lyrics = lyrics.replace("picket sign", "protest")

    # Normalizing terms for `Vietnam`
    lyrics = lyrics.replace("viet cong", "vietnam")
    lyrics = lyrics.replace(" nam ", "vietnam")
    lyrics = lyrics.replace("'nam", "vietnam")
    lyrics = lyrics.replace("vietnamese", "vietnam")

    # Normalizing terms for `president`
    lyrics = lyrics.replace("chief", "president")
    lyrics = lyrics.replace("presidential", "president")
    lyrics = lyrics.replace("lyndon johnson", "president")
    lyrics = lyrics.replace("lbj", "president")
    lyrics = lyrics.replace("nixon", "president")
    lyrics = lyrics.replace("richard nixon", "president")
    lyrics = lyrics.replace("donald trump", "president")

    # Normalizing terms for `communism`
    lyrics = lyrics.replace("communist", "communism")
    lyrics = lyrics.replace("commie", "communism")

    # Normalizing terms for `America`
    lyrics = lyrics.replace("usa", "america")
    lyrics = lyrics.replace("united states", "america")
    lyrics = lyrics.replace("uncle sam", "america")
    lyrics = lyrics.replace("american", "america")
    lyrics = lyrics.replace("red white and blue", "america")
    lyrics = lyrics.replace("red white blue", "america")

    # Normalziing terms for `MAGA`
    lyrics = lyrics.replace("make america great", "maga")
    lyrics = lyrics.replace("making america great", "maga")

    # Normalizing terms for `red hat`
    lyrics = lyrics.replace("maga hat", "red hat")
    lyrics = lyrics.replace("red cap", "red hat")
    lyrics = lyrics.replace("racist hat", "red hat")

    # Normalizing terms for `the wall`
    lyrics = lyrics.replace("walls", "the wall")
    lyrics = lyrics.replace("wall", "the wall")

    # Normalizing terms for `Mexico`
    lyrics = lyrics.replace("mexican", "mexico")
    lyrics = lyrics.replace("mexicans", "mexico")

    # Normalizing terms for `racism`
    lyrics = lyrics.replace("racist", "racism")

    # Normalizing terms for `fascism`
    lyrics = lyrics.replace("fascist", "fascism")






    lyrics = lyrics.strip()
    
    return lyrics
