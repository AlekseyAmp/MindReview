export function getSentimentInfo(sentiment) {
    switch (sentiment) {
        case 'Нейтральный':
            return { color: '#E56935', emoji: 'img/icons/neutral-emoji.svg' };
        case 'Позитивный':
            return { color: '#15966E', emoji: 'img/icons/happy-emoji.svg' };
        case 'Негативный':
            return { color: '#eb0b0b', emoji: 'img/icons/angry-emoji.svg' };
        default:
            return null;
    }
};
