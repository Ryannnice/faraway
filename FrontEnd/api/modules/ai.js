import { backendFirst } from '../request'

export function generateStrategy(payload) {
  return backendFirst({
    url: '/api/ai/generate-strategy',
    method: 'POST',
    data: payload,
    timeout: 60000
  }, () => ({
    destination: payload.destination,
    overview: `${payload.destination} 适合 ${payload.days || 3} 天慢节奏旅行，推荐以风景、在地美食和夜晚散步为主线。`,
    dailyPlans: [
      {
        day: 1,
        activities: ['抵达后入住并轻松逛主城区', '傍晚去高点看日落', '夜里体验当地小馆'],
        food: ['在地早餐', '街头小吃'],
        accommodation: '靠近交通节点的安静酒店'
      },
      {
        day: 2,
        activities: ['主景点深度游', '拍照路线', '河边或海边散步'],
        food: ['人气咖啡馆', '晚餐预约餐厅'],
        accommodation: '原酒店续住'
      }
    ],
    tips: ['提前看天气再决定穿搭', '尽量把热门景点放在清晨或傍晚', '给自己留一点自由发呆时间']
  }), 600)
}
