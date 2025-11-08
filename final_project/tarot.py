from flask import Flask, render_template, jsonify

# 初始化 Flask 應用
app = Flask(__name__)

def create_full_deck():
    """
    在 Python 中產生完整的 78 張塔羅牌
    """
    deck = []
    suits = ['Wands', 'Cups', 'Swords', 'Pentacles']
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Page', 'Knight', 'Queen', 'King']
    major_arcana_names = [
        'The Fool', 'The Magician', 'The High Priestess', 'The Empress', 'The Emperor',
        'The Hierophant', 'The Lovers', 'The Chariot', 'Strength', 'The Hermit',
        'Wheel of Fortune', 'Justice', 'The Hanged Man', 'Death', 'Temperance',
        'The Devil', 'The Tower', 'The Star', 'The Moon', 'The Sun', 'Judgement', 'The World'
    ]
    major_arcana_names_zh = [
        '愚者', '魔術師', '女祭司', '皇后', '皇帝', '教皇', '戀人', '戰車', '力量', '隱士',
        '命運之輪', '正義', '吊人', '死神', '節制', '惡魔', '高塔', '星星', '月亮', '太陽', '審判', '世界'
    ]
    
    id_counter = 0

    # 加入大阿爾克那
    for i in range(len(major_arcana_names)):
        deck.append({
            'id': id_counter,
            'name': major_arcana_names_zh[i],
            'en': major_arcana_names[i],
            'type': 'major'
        })
        id_counter += 1

    # 加入小阿爾克那
    suit_map_zh = {
        'Wands': '權杖',
        'Cups': '聖杯',
        'Swords': '寶劍',
        'Pentacles': '錢幣'
    }
    
    rank_map_zh = {
        'Ace': 'A',
        'Page': '侍者',
        'Knight': '騎士',
        'Queen': '皇后',
        'King': '國王'
    }

    for suit in suits:
        suit_zh = suit_map_zh.get(suit)
        
        for rank in ranks:
            # 獲取中文階級，如果不在 map 中，則使用原來的數字
            rank_zh = rank_map_zh.get(rank, rank)

            deck.append({
                'id': id_counter,
                'name': f'{suit_zh} {rank_zh}',
                'en': f'{rank} of {suit}',
                'type': 'minor'
            })
            id_counter += 1
            
    return deck # 總共 78 張牌

@app.route('/')
def index():
    """
    渲染主頁面 (index.html)
    """
    # Flask 會自動在 'templates' 資料夾中尋找
    return render_template('index.html')

@app.route('/api/deck')
def get_deck():
    """
    提供牌組資料的 API 接口
    """
    deck = create_full_deck()
    # 將 Python 列表轉換為 JSON 格式回傳
    return jsonify(deck)

if __name__ == '__main__':
    # 啟動伺服器
    app.run(debug=True)
