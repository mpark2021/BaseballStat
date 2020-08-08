import urllib.request as request
from utility.pid_helper import espn_to_fangraph


def load_data(season):
    url = "http://www.espn.com/mlb/freeagents/_/year/{0}/type/dollars"
    url = url.format(season)
    page = request.urlopen(url)
    read = page.read()
    try:
        data = read.decode('utf-8')
    except UnicodeDecodeError:
        data = read.decode('latin-1')
        data = data.replace('é', 'e')

    return data


def split_attributes(tag):
    attributes = tag.split()
    is_open = False

    merge_list = []

    for i, attr in enumerate(attributes):
        if '"' in attr and attr.count('"') == 1:
            is_open = not is_open
            merge_list.append(i)

    # 이 시점에서 is_open은 반드시 False여야한다
    i = 0
    result = []
    while i < len(attributes):
        if len(merge_list) > 0 and i == merge_list[0]:
            start = merge_list.pop(0)
            end = merge_list.pop(0)
            temp = ""
            for i in range(start, end + 1):
                temp += attributes[i] + " "
            result.append(temp[:-1])
            i = end + 1
        else:
            result.append(attributes[i])
            i += 1

    return result


def cut_tag(contents, tag, class_name=None, exact=False):
    # <tag />
    # <tag attr1="blah" attr2="blah"> content </tag>
    start = contents.find("<" + tag)
    # to include </tag>
    end = contents.find("</" + tag) + (2 + 1 + len(tag))

    if class_name is not None:
        while start != -1 and end != -1:
            temp = contents[start:end]
            attribute = split_attributes(temp[1:temp.find(">")])
            for attr in attribute:
                if "class=" in attr:
                    c = attr.split("class=")[1]
                    if not exact and class_name in c:
                        return temp, start, end
                    # to remove quotes, use c[1:-1]
                    if exact and class_name == c[1:-1]:
                        return temp, start, end

            # after </tag>
            contents = contents[end:]
            start = contents.find("<" + tag)
            end = contents.find("</" + tag) + (2 + 1 + len(tag))

        return "", -1, -1

    return contents[start:end], start, end


def split_tags(contents, tag):
    result = []
    start = contents.find("<" + tag)
    end = contents.find("</" + tag) + (2 + 1 + len(tag))
    while start != -1 and end != -1:
        result.append(contents[start:end])
        contents = contents[end:]
        start = contents.find("<" + tag)
        end = contents.find("</" + tag) + (2 + 1 + len(tag))

    return result


def parse_contract(season):
    raw = load_data(season)
    table, _, _ = cut_tag(raw, "table")
    players = []
    p, start, end = cut_tag(table, "tr", "player")
    while start != -1 and end != -1:
        if p not in players:
            players.append(p)
        table = table[end:]
        p, start, end = cut_tag(table, "tr", "player")

    result = []
    for p in players:
        data = split_tags(p, "td")
        result.append(PlayerData(data))

    return result

pos = ['SP', 'RP', '1B', '2B', '3B', 'SS', 'RF', 'CF', 'LF', 'C', 'DH', 'OF', 'P']


class PlayerData:
    def __init__(self, data):
        data = list(map(self._process, data))
        data[0] = self._process(data[0])
        self.name = data[0]
        if self.name == "Jose Molina":
            self.position = "C"
        else:
            self.position = data[1]
        self.age = int(data[2])
        self.status = data[3]
        self.prior_team = data[4]
        self.new_team = data[5]
        if len(data[6]) > 0:
            self.contract_years = int(data[6])
        else:
            self.contract_years = 0

        if data[8][0] == "$":
            self.dollars = ""
            dollar_str = data[8]
            for s in dollar_str.split(','):
                self.dollars += s
            self.dollars = int(self.dollars[1:])
        else:
            self.dollars = 0

    def is_signed(self):
        return self.status == 'Signed' and self.contract_years > 0 and self.dollars > 0 and\
               self.prior_team not in ['--', 'Japan', 'Cuba']

    def is_batter(self):
        return not self.is_pitcher()

    def is_pitcher(self):
        return self.position == "SP" or self.position == "RP" or self.position == "P"

    def get_position(self):
        # P and OF are exceptions...
        return pos.index(self.position)

    def get_name(self):
        return espn_to_fangraph(self.name)

    @staticmethod
    def _process(data):
        start = data.find(">")
        end = data.find("</")
        if end == -1:
            return data[start + 1:]

        return data[start + 1:end]


if __name__ == "__main__":
    result = parse_contract(2019)
    for pd in result:
        if not pd.is_signed():
            print(pd.name)