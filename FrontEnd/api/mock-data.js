export const currentUser = {
  id: 1,
  nickname: '远方旅客',
  avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=600',
  bio: '探索未知的旅人，偏爱冷色海风与漫长火车线。',
  stats: {
    posts: 18,
    favorites: 42,
    likes: 96,
    matches: 3
  }
}

export const guestUsers = [
  {
    id: 2,
    nickname: '城市夜行者',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=600',
    bio: '偏爱夜色、霓虹和凌晨一点的便利店。'
  },
  {
    id: 3,
    nickname: '云端旅人',
    avatar: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&q=80&w=600',
    bio: '雪线以上的风景，是我最稳定的情绪来源。'
  },
  {
    id: 4,
    nickname: '海边的卡夫卡',
    avatar: 'https://images.unsplash.com/photo-1504593811423-6dd665756598?auto=format&fit=crop&q=80&w=600',
    bio: '喜欢长堤、海风、独处和有回声的黄昏。'
  }
]

function getAuthor(index) {
  return [currentUser, ...guestUsers][index % 4]
}

function parseCount(value) {
  if (typeof value === 'number') {
    return value
  }
  if (String(value).includes('w')) {
    return Math.round(parseFloat(String(value)) * 10000)
  }
  if (String(value).includes('k')) {
    return Math.round(parseFloat(String(value)) * 1000)
  }
  return Number(value || 0)
}

export const strategies = [
  {
    id: 101,
    title: '冰岛：在世界尽头寻找那一抹永恒的蓝',
    summary: '冰川、黑沙滩、瀑布，这是一场通往星球实验室的旅行。',
    content: '冰岛是一个充满自然奇观的国家。从震撼的瀑布到神秘的黑沙滩，每一处景色都让人流连忘返。建议租一辆四驱车沿着一号公路自驾，冬季守极光，夏季看瀑布和冰河湖。',
    destination: '冰岛',
    category: '自然风光',
    days: 5,
    coverUrl: 'https://images.unsplash.com/photo-1476610182048-b716b8518aae?auto=format&fit=crop&q=80&w=2000',
    tags: ['深度游', '冰川', '极光'],
    author: getAuthor(0),
    likeCount: 1123,
    favoriteCount: 1200,
    viewCount: parseCount('2.4w'),
    createdAt: '2026-04-20'
  },
  {
    id: 102,
    title: '东京：深夜食堂里的城市灵魂',
    summary: '在这里，每一碗拉面都有故事。挖掘那些不为人知的巷弄美食。',
    content: '东京不仅仅是国际化大都市，更是吃货的天堂。筑地市场、新宿黄金街和银座拉面店，是这一版路线的核心支点。',
    destination: '东京',
    category: '美食地图',
    days: 4,
    coverUrl: 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&q=80&w=2000',
    tags: ['美食探店', '夜游', '城市'],
    author: getAuthor(1),
    likeCount: 860,
    favoriteCount: 950,
    viewCount: parseCount('1.8w'),
    createdAt: '2026-04-18'
  },
  {
    id: 103,
    title: '海岛清单：不失格调的极简主义',
    summary: '如何用最少的行李拍出大片感。享受纯粹的碧海蓝天。',
    content: '马尔代夫极简之旅最重要的是舍弃冗余装备，只留下会真正让你舒服和出片的那部分。水上屋、无人岛和夜间海钓就够了。',
    destination: '马尔代夫',
    category: '自然风光',
    days: 4,
    coverUrl: 'https://images.unsplash.com/photo-1506929113614-bb4014906bb1?auto=format&fit=crop&q=80&w=2000',
    tags: ['极简旅行', '海岛', '度假'],
    author: getAuthor(2),
    likeCount: 920,
    favoriteCount: 2100,
    viewCount: parseCount('3.2w'),
    createdAt: '2026-04-17'
  },
  {
    id: 104,
    title: '巅峰之旅：喜马拉雅徒步完全手册',
    summary: '专为探险家准备的极高海拔生存指南。',
    content: '这是一场身体与心灵的双重考验。冈仁波齐转山和纳木错环湖都很值得，但务必准备高质量冲锋衣、防晒和充足补给。',
    destination: '西藏',
    category: '自然风光',
    days: 7,
    coverUrl: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=2000',
    tags: ['硬核户外', '徒步', '高海拔'],
    author: getAuthor(3),
    likeCount: 1480,
    favoriteCount: 4800,
    viewCount: parseCount('5.6w'),
    createdAt: '2026-04-16'
  },
  {
    id: 105,
    title: '巴黎：流动在左岸的艺术盛宴',
    summary: '卢浮宫之外，还有哪些值得一读的艺术空间？',
    content: '巴黎的每一条街道都充满艺术气息。奥赛、蓬皮杜和橘园美术馆，是比打卡更值得慢慢消化的部分。',
    destination: '巴黎',
    category: '人文历史',
    days: 3,
    coverUrl: 'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&q=80&w=2000',
    tags: ['艺术修养', '博物馆', '左岸'],
    author: getAuthor(0),
    likeCount: 760,
    favoriteCount: 1400,
    viewCount: parseCount('2.1w'),
    createdAt: '2026-04-15'
  },
  {
    id: 106,
    title: '京都：在碎石小径里遇见一千年前的夏天',
    summary: '和服、禅意花园、抹茶香，这是时间留下的温柔。',
    content: '清晨去岚山竹林，中午在茶室慢下来，傍晚去花见小路散步。京都不是用来赶景点的，是用来慢慢体会的。',
    destination: '京都',
    category: '人文历史',
    days: 3,
    coverUrl: 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&q=80&w=2000',
    tags: ['古风摄影', '慢旅行', '抹茶'],
    author: getAuthor(1),
    likeCount: 1660,
    favoriteCount: 3100,
    viewCount: parseCount('4.5w'),
    createdAt: '2026-04-14'
  },
  {
    id: 107,
    title: '圣托里尼：属于爱琴海的蓝白协奏曲',
    summary: '日落时分，整个世界都温柔了下来。',
    content: '蓝顶教堂和白房子只是起点，真正值得的是在日落前去伊亚镇高处等光线慢慢退场。',
    destination: '圣托里尼',
    category: '自然风光',
    days: 3,
    coverUrl: 'https://images.unsplash.com/photo-1570071437642-85623bf657dd?auto=format&fit=crop&q=80&w=2000',
    tags: ['浪漫胜地', '日落', '爱琴海'],
    author: getAuthor(2),
    likeCount: 970,
    favoriteCount: 1900,
    viewCount: parseCount('2.7w'),
    createdAt: '2026-04-13'
  },
  {
    id: 108,
    title: '瑞士：坐着火车去云端，开启森林童话',
    summary: '阿尔卑斯山的积雪，是大地写给天空的情书。',
    content: '瑞士最完善的交通方式就是火车。金色山口列车和少女峰铁道都值得留出整块时间，不要匆忙。',
    destination: '瑞士',
    category: '自然风光',
    days: 5,
    coverUrl: 'https://images.unsplash.com/photo-1502404689324-745849d79c3d?auto=format&fit=crop&q=80&w=2000',
    tags: ['亲子旅游', '火车', '雪山'],
    author: getAuthor(3),
    likeCount: 1920,
    favoriteCount: 5100,
    viewCount: parseCount('6.2w'),
    createdAt: '2026-04-12'
  },
  {
    id: 109,
    title: '马丘比丘：失落的高原文明',
    summary: '在安第斯山脉之巅，见证印加帝国的辉煌余韵。',
    content: '马丘比丘适合把路程本身也当成体验的一部分。热水镇过夜再清晨上山，会比赶时间舒服很多。',
    destination: '秘鲁',
    category: '人文历史',
    days: 4,
    coverUrl: 'https://images.unsplash.com/photo-1587590227264-0ac64ce63ce8?auto=format&fit=crop&q=80&w=2000',
    tags: ['历史探踪', '高原', '文明'],
    author: getAuthor(0),
    likeCount: 640,
    favoriteCount: 880,
    viewCount: parseCount('1.2w'),
    createdAt: '2026-04-11'
  },
  {
    id: 110,
    title: '首尔：24小时不夜城的硬核穿搭指南',
    summary: '从东大门到弘大，哪里才是弄潮儿的真爱？',
    content: '从新沙洞到圣水洞，首尔最适合边逛边拍。穿搭、咖啡馆和小众买手店可以组合成一条很完整的路线。',
    destination: '首尔',
    category: '美食地图',
    days: 3,
    coverUrl: 'https://images.unsplash.com/photo-1518391846015-55a9cc003b25?auto=format&fit=crop&q=80&w=2000',
    tags: ['时尚购物', '街拍', '夜生活'],
    author: getAuthor(1),
    likeCount: 720,
    favoriteCount: 1100,
    viewCount: parseCount('3.9w'),
    createdAt: '2026-04-10'
  },
  {
    id: 111,
    title: '撒哈拉：在三毛笔下的沙漠做一场金色的梦',
    summary: '每一粒沙，都藏着自由的灵魂。',
    content: '骑骆驼看日落和沙漠露营都值得体验一次。真正难忘的是凌晨出帐篷时看到的星空。',
    destination: '摩洛哥',
    category: '自然风光',
    days: 4,
    coverUrl: 'https://images.unsplash.com/photo-1509216242873-7786f446f465?auto=format&fit=crop&q=80&w=2000',
    tags: ['异域风情', '沙漠', '星空'],
    author: getAuthor(2),
    likeCount: 880,
    favoriteCount: 1600,
    viewCount: parseCount('2.5w'),
    createdAt: '2026-04-09'
  },
  {
    id: 112,
    title: '挪威：驾车穿梭于峡湾与森林的静谧之间',
    summary: '自驾爱好者的终极乐园，每一帧都是壁纸。',
    content: '沿着大西洋公路前行，景观本身就是路线的一部分。老鹰之路和卑尔根适合作为两种完全不同节奏的停靠点。',
    destination: '挪威',
    category: '摄影攻略',
    days: 6,
    coverUrl: 'https://images.unsplash.com/photo-1544085311-11a028465b0c?auto=format&fit=crop&q=80&w=2000',
    tags: ['自驾摄影', '峡湾', '森林'],
    author: getAuthor(3),
    likeCount: 1210,
    favoriteCount: 3400,
    viewCount: parseCount('4.1w'),
    createdAt: '2026-04-08'
  }
]

export const vlogs = [
  {
    id: 201,
    type: 'vlog',
    title: '孤独的星球：午夜的冰川之歌',
    content: '在这里，时间仿佛静止。#冰岛旅行',
    location: '冰岛 · 杰古沙龙冰河湖',
    coverUrl: 'https://images.unsplash.com/photo-1476610182048-b716b8518aae?auto=format&fit=crop&q=80&w=2000',
    mediaList: [{ type: 'video', url: 'https://69ef0ab2abe5326bdb41ee67.imgix.net/running.mp4' }],
    tags: ['冰岛', '旅行', '冰川', '自然'],
    author: {
      id: 5,
      nickname: '林间拾光',
      avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&q=80&w=600'
    },
    likeCount: parseCount('2.4w'),
    favoriteCount: parseCount('8.9k'),
    playCount: 74000,
    createdAt: '2026-04-22'
  },
  {
    id: 202,
    type: 'vlog',
    title: '逃离城市：苍山洱海边的慢生活',
    content: '在洱海边骑行，听风的声音。#大理 #慢生活',
    location: '大理 · 洱海',
    coverUrl: 'https://images.unsplash.com/photo-1590483734724-383b853b278a?auto=format&fit=crop&q=80&w=2000',
    mediaList: [{ type: 'video', url: 'https://69ef0ab2abe5326bdb41ee67.imgix.net/paraglider.mp4' }],
    tags: ['大理', '慢生活', '文艺', '风光'],
    author: {
      id: 6,
      nickname: '阿远在路上',
      avatar: 'https://images.unsplash.com/photo-1546961329-78bef0414d7c?auto=format&fit=crop&q=80&w=600'
    },
    likeCount: parseCount('1.2w'),
    favoriteCount: parseCount('4.5k'),
    playCount: 52000,
    createdAt: '2026-04-21'
  },
  {
    id: 203,
    type: 'vlog',
    title: '日照金山：神山的终极浪漫',
    content: '凌晨四点的等待。#川西 #贡嘎',
    location: '川西 · 贡嘎雪山',
    coverUrl: 'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&q=80&w=2000',
    mediaList: [{ type: 'video', url: 'https://player.vimeo.com/external/441433605.sd.mp4?s=ef77732d8471191024328574c76b9ee610f4aff2&profile_id=139&oauth2_token_id=57447761' }],
    tags: ['川西', '雪山', '探索'],
    author: {
      id: 7,
      nickname: '山野寻踪',
      avatar: 'https://images.unsplash.com/photo-1504257432389-52343af06ae3?auto=format&fit=crop&q=80&w=600'
    },
    likeCount: parseCount('4.8w'),
    favoriteCount: parseCount('1.2w'),
    playCount: 128000,
    createdAt: '2026-04-20'
  },
  {
    id: 204,
    type: 'vlog',
    title: '海边的琴声：在孤独中寻找自由',
    content: '面朝大海。#阿那亚',
    location: '阿那亚 · 孤独图书馆',
    coverUrl: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&q=80&w=2000',
    mediaList: [{ type: 'video', url: 'https://player.vimeo.com/external/371434633.sd.mp4?s=9852f6f59995574c861e680a6c2fc4ef006af8b3&profile_id=139&oauth2_token_id=57447761' }],
    tags: ['海边', '阿那亚', '孤独', '艺术'],
    author: getAuthor(3),
    likeCount: parseCount('8.2k'),
    favoriteCount: parseCount('3.1k'),
    playCount: 43000,
    createdAt: '2026-04-19'
  },
  {
    id: 205,
    type: 'vlog',
    title: '迷失在世界上最蓝的小镇',
    content: '天空的颜色。#舍夫沙万 #摩洛哥',
    location: '摩洛哥 · 舍夫沙万',
    coverUrl: 'https://images.unsplash.com/photo-1509216242873-7786f446f465?auto=format&fit=crop&q=80&w=2000',
    mediaList: [{ type: 'video', url: 'https://player.vimeo.com/external/403810232.sd.mp4?s=d00cf0f230232e01df332616215160c8e23e2060&profile_id=139&oauth2_token_id=57447761' }],
    tags: ['摩洛哥', '色彩', '异域', '蓝'],
    author: getAuthor(1),
    likeCount: parseCount('3.5w'),
    favoriteCount: parseCount('7.2k'),
    playCount: 86000,
    createdAt: '2026-04-18'
  },
  {
    id: 206,
    type: 'vlog',
    title: '极光爆发夜：欧若拉的裙摆',
    content: '零下30度的坚守。#极光 #芬兰',
    location: '芬兰 · 拉普兰',
    coverUrl: 'https://images.unsplash.com/photo-1531366930477-4fbd0f06a310?auto=format&fit=crop&q=80&w=2000',
    mediaList: [{ type: 'video', url: 'https://player.vimeo.com/external/459389137.sd.mp4?s=9944075416039535e617d3d7ba119c629fb63d27&profile_id=139&oauth2_token_id=57447761' }],
    tags: ['芬兰', '极光', '冬日', '梦幻'],
    author: {
      id: 8,
      nickname: '极光猎人',
      avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=600'
    },
    likeCount: parseCount('12w'),
    favoriteCount: parseCount('4.5w'),
    playCount: 220000,
    createdAt: '2026-04-17'
  }
]

export const notices = [
  { id: 1, type: 'like', title: '有人点赞了你的 Vlog《日照金山：神山的终极浪漫》', targetId: 203, createdAt: '2026-04-26 10:30' },
  { id: 2, type: 'favorite', title: '有人收藏了你的攻略《京都：在碎石小径里遇见一千年前的夏天》', targetId: 106, createdAt: '2026-04-25 19:20' },
  { id: 3, type: 'system', title: '新的版本即将开放更多上传能力', targetId: 0, createdAt: '2026-04-25 18:20' }
]

export const interactionState = {
  likedStrategies: [101, 106],
  favoritedStrategies: [102, 107],
  likedVlogs: [202, 205],
  favoritedVlogs: [201, 206],
  strategyComments: {
    101: [
      {
        id: 1,
        userId: 2,
        nickname: '城市夜行者',
        avatar: guestUsers[0].avatar,
        content: '冰岛这条线看起来太适合第一次自驾了。',
        createdAt: '2026-04-26 09:10'
      }
    ],
    106: [
      {
        id: 2,
        userId: 3,
        nickname: '云端旅人',
        avatar: guestUsers[1].avatar,
        content: '京都真的适合慢慢走，这条路线很对味。',
        createdAt: '2026-04-25 20:30'
      }
    ]
  },
  postComments: {
    201: [
      {
        id: 11,
        userId: 4,
        nickname: '海边的卡夫卡',
        avatar: guestUsers[2].avatar,
        content: '这个风感太好了，适合循环看。',
        createdAt: '2026-04-26 11:20'
      }
    ],
    202: [
      {
        id: 12,
        userId: 2,
        nickname: '城市夜行者',
        avatar: guestUsers[0].avatar,
        content: '滑到这里的时候真的有点想立刻出发。',
        createdAt: '2026-04-25 18:05'
      }
    ]
  },
  strategyShareCount: {
    101: 32,
    102: 18,
    106: 24
  },
  postShareCount: {
    201: 46,
    202: 33,
    205: 27
  }
}

export const drafts = [
  { id: 1, draftType: 'strategy', title: '北海道冬日草稿', updatedAt: '2026-04-25 13:00' },
  { id: 2, draftType: 'post', title: '海边清晨 Vlog 草稿', updatedAt: '2026-04-24 19:20' }
]

export const matchRecruitments = [
  {
    id: 301,
    publisherUserId: 2,
    destination: '大理',
    startDate: '2026-05-01',
    days: 3,
    status: 'open',
    createdAt: '2026-04-26 19:20'
  },
  {
    id: 302,
    publisherUserId: 3,
    destination: '冰岛',
    startDate: '2026-05-08',
    days: 5,
    status: 'open',
    createdAt: '2026-04-26 14:10'
  },
  {
    id: 303,
    publisherUserId: 4,
    destination: '京都',
    startDate: '2026-05-10',
    days: 2,
    status: 'open',
    createdAt: '2026-04-25 21:05'
  }
]

export const matchApplications = [
  {
    id: 401,
    recruitId: 301,
    publisherUserId: 2,
    applicantUserId: 1,
    status: 'pending',
    createdAt: '2026-04-27 09:40'
  },
  {
    id: 402,
    recruitId: 302,
    publisherUserId: 3,
    applicantUserId: 1,
    status: 'approved',
    createdAt: '2026-04-26 18:00'
  },
  {
    id: 403,
    recruitId: 303,
    publisherUserId: 4,
    applicantUserId: 2,
    status: 'pending',
    createdAt: '2026-04-27 10:20'
  }
]

export const searchHistorySeed = ['大理', '京都夜色', '冰岛', '雪山徒步']

export const hotKeywords = [
  '大理',
  '冰岛',
  '京都',
  '东京夜游',
  '雪山徒步',
  '海岛旅行',
  '摩洛哥蓝镇',
  '芬兰极光'
]
