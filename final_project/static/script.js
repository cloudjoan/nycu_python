// static/script.js

// 將 fullDeck 宣告在頂層，以便所有函式都能存取
let fullDeck = [];

// 獲取 DOM 元素
const spreadArea = document.getElementById('spread-area');
const selectionArea = document.getElementById('selection-area');
const drawButton = document.getElementById('draw-btn');

let selectedCardsData = []; 
const maxSelection = 5;

/**
 * 非同步啟動函式
 * 頁面載入時執行
 */
async function initializeApp() {
    // 1. 從 Python 後端獲取牌組資料
    try {
        const response = await fetch('/api/deck'); // 呼叫 app.py 中的 API
        if (!response.ok) {
            throw new Error('無法獲取牌組資料');
        }
        fullDeck = await response.json(); // 將 JSON 資料存入全域變數
        
        // 2. 綁定按鈕事件
        drawButton.addEventListener('click', initializeDeck);
        
        // 3. 頁面載入時自動攤牌一次
        initializeDeck();
        
    } catch (error) {
        console.error("初始化失敗:", error);
        spreadArea.innerHTML = `<p style="color: #f87171; text-align: center;">無法載入牌組。請檢查後端伺服器是否正在運行。</p>`;
    }
}

/**
 * 攤牌函式
 * 負責洗牌、建立卡槽、並執行攤牌動畫
 */
function initializeDeck() {
    // 1. 清空區域
    spreadArea.innerHTML = '';
    selectionArea.innerHTML = '';
    selectedCardsData = []; 
    
    // 重置 selectionArea 的樣式
    selectionArea.style.paddingTop = ''; 
    selectionArea.style.height = '';

    // 2. 檢查 fullDeck 是否已載入
    if (fullDeck.length === 0) {
        console.error("牌組尚未載入");
        return;
    }

    // 3. 隨機洗牌 (Fisher-Yates 演算法)
    let shuffledDeck = [...fullDeck];
    for (let i = shuffledDeck.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffledDeck[i], shuffledDeck[j]] = [shuffledDeck[j], shuffledDeck[i]];
    }

    // 4. 建立下方的選擇卡槽
    let needsPadding = false; 
    for (let i = 0; i < maxSelection; i++) {
        const slot = document.createElement('div');
        slot.classList.add('slot');

        if (i === 0 || i === (maxSelection - 1)) { // i=0 (第一張) 或 i=4 (第五張)
            slot.style.transform = 'translateY(-30%)'; // 高出 30%
            needsPadding = true;
        }

        slot.dataset.slotIndex = i;
        slot.innerText = `第 ${i + 1} 張`;
        selectionArea.appendChild(slot);
    }

    // 統一調整外層容器 (*** 修正 '}' 錯誤 ***)
    if (needsPadding) { 
        selectionArea.style.paddingTop = '60px'; 
        selectionArea.style.height = 'auto'; 
    }

    // 5. 建立並攤開卡牌 (*** 中央拱橋 ***)
    const totalCards = shuffledDeck.length; 
    const arcWidth = 170; // 拱橋總角度 (170度)
    const angleStep = arcWidth / (totalCards - 1);
    
    shuffledDeck.forEach((cardData, i) => {
        const cardEl = document.createElement('div');
        cardEl.classList.add('card');
        cardEl.dataset.cardId = cardData.id; 
        
        // 建立卡牌的 HTML 結構 (正反面)
        cardEl.innerHTML = `
            <div class="card-inner">
                <div class="card-back"></div>
                <div class="card-front"></div> 
            </div>
        `;

        // 攤牌動畫 (*** 中央拱橋效果 ***)
        // 牌的初始位置 left: 10% (由 style.css 定義)
        // JS 在此將其動畫到 left: 50% 並套用旋轉
        setTimeout(() => {
            const angle = (i - (totalCards - 1) / 2) * angleStep; // 計算每張牌的角度
            const translateY = Math.abs(angle) * 2.5; // 角度越大，Y位移越多，形成拱形
            cardEl.style.left = '50%'; // 最終水平位置 (中央)
            cardEl.style.transform = `translateX(-50%) rotate(${angle}deg) translateY(-${translateY}px)`;
        }, i * 20); // 錯開時間以產生動畫

        // 綁定點擊事件
        cardEl.addEventListener('click', handleCardClick);
        spreadArea.appendChild(cardEl);
    });
}

/**
 * 選牌函式
 * 處理點擊攤開的卡牌，並執行飛行動畫
 */
function handleCardClick(event) {
    if (selectedCardsData.length >= maxSelection) return;
    const clickedCardEl = event.currentTarget;
    if (clickedCardEl.classList.contains('is-selected')) return;

    // 1. 標記原卡牌為已選
    clickedCardEl.classList.add('is-selected'); 

    // 2. 獲取卡牌資料和目標卡槽
    const cardId = parseInt(clickedCardEl.dataset.cardId);
    const cardData = fullDeck.find(c => c.id === cardId); 
    const selectionIndex = selectedCardsData.length;
    selectedCardsData.push(cardData);

    const targetSlot = document.querySelector(`.slot[data-slot-index="${selectionIndex}"]`);
    if (!targetSlot) return;

    // --- 飛行動畫開始 ---

    // 3. 獲取起始/結束位置
    const cardRect = clickedCardEl.getBoundingClientRect();
    const slotRect = targetSlot.getBoundingClientRect();

    // 4. 建立 "飛行卡" (牌背)
    const flyingCard = document.createElement('div');
    flyingCard.classList.add('flying-card'); 
    // (*** 修正拼寫錯誤 ***)
    flyingCard.innerHTML = `
        <div class="card-inner">
            <div class="card-back"></div>
        </div>
    `;
    
    // 5. 設定 "飛行卡" 初始位置
    flyingCard.style.left = `${cardRect.left}px`;
    flyingCard.style.top = `${cardRect.top}px`;
    flyingCard.style.transform = clickedCardEl.style.transform; 
    document.body.appendChild(flyingCard);

    // 6. 準備好在卡槽中的 "真實" 卡牌，但先隱藏
    const imgUrl = `https://placehold.co/120x160/2a2a3a/ffffff?text=${encodeURIComponent(cardData.name)}`; // 確保中文名正確
    const cardInSlot = document.createElement('div');
    cardInSlot.classList.add('card');
    cardInSlot.style.width = '100%';
    cardInSlot.style.height = '100%';
    cardInSlot.style.cursor = 'pointer'; 
    cardInSlot.style.opacity = 0; // 初始隱藏
    cardInSlot.style.position = 'relative';

    // 填入 "真實" 卡牌的內容 (正反面)
    // (*** 修正拼寫錯誤 ***)
    cardInSlot.innerHTML = `
        <div class="card-inner">
            <div class="card-back"></div>
            <div class="card-front">
                <img src="${imgUrl}" alt="${cardData.name}">
                <div class="card-front-name">${cardData.name}</div>
            </div>
        </div>
    `;

    // 將 "真實" 卡牌放入卡槽
    targetSlot.innerHTML = ''; 
    targetSlot.appendChild(cardInSlot); 
    // targetSlot.style.border = 'none'; 
    targetSlot.style.padding = '0'; 

    // 7. 觸發 "飛行" 動畫
    requestAnimationFrame(() => {
        // 計算目標位置 (卡槽中心)
        const targetLeft = slotRect.left + (slotRect.width - 100) / 2;
        const targetTop = slotRect.top + (slotRect.height - 170) / 2;
        
        flyingCard.style.left = `${targetLeft}px`;
        flyingCard.style.top = `${targetTop}px`;
        flyingCard.style.transform = `rotate(0deg) scale(${slotRect.width / 100})`; 
    });

    // 8. 等待動畫結束 (1200ms)
    setTimeout(() => {
        flyingCard.remove(); // 移除 "飛行卡"
        
        // 顯示 "真實" 卡牌
        cardInSlot.style.opacity = 1; 
        cardInSlot.style.transition = 'opacity 0.2s'; 
        
        // *** 關鍵：自動翻牌 ***
        // 稍微延遲 (50ms) 後，加入 .is-flipped 觸發 CSS 翻牌動畫
        setTimeout(() => { 
             cardInSlot.classList.add('is-flipped'); // 翻牌
        }, 50);
       
        // 綁定翻轉事件 (讓卡槽中的牌可以來回翻)
        cardInSlot.addEventListener('click', () => {
            cardInSlot.classList.toggle('is-flipped'); 
        });
    }, 2000); // 必須匹配 CSS 中的 1.2s
}

// 頁面載入時呼叫啟動函式
initializeApp();

