import { backendFirst } from '../request'
import { currentUser, guestUsers, matchApplications, matchRecruitments } from '../mock-data'

function getUsers() {
  return [currentUser, ...guestUsers]
}

function findUser(userId) {
  return getUsers().find((item) => Number(item.id) === Number(userId)) || currentUser
}

function findRecruitment(recruitId) {
  return matchRecruitments.find((item) => Number(item.id) === Number(recruitId))
}

function getNextRecruitmentId() {
  return matchRecruitments.reduce((max, item) => Math.max(max, Number(item.id) || 0), 300) + 1
}

function getNextApplicationId() {
  return matchApplications.reduce((max, item) => Math.max(max, Number(item.id) || 0), 400) + 1
}

function getNowLabel() {
  return '刚刚'
}

function getApplicationForCurrentUser(recruitId) {
  return matchApplications.find((item) => Number(item.recruitId) === Number(recruitId) && Number(item.applicantUserId) === Number(currentUser.id))
}

function buildRecommendedCard(recruitment) {
  const publisher = findUser(recruitment.publisherUserId)
  const application = getApplicationForCurrentUser(recruitment.id)
  return {
    recruitId: recruitment.id,
    publisherUserId: publisher.id,
    publisherNickname: publisher.nickname,
    publisherAvatar: publisher.avatar,
    destination: recruitment.destination,
    startDate: recruitment.startDate,
    days: recruitment.days,
    applicationStatus: application ? application.status : 'none',
    createdAt: recruitment.createdAt
  }
}

function buildMyRecruitment(recruitment) {
  const applications = matchApplications
    .filter((item) => Number(item.recruitId) === Number(recruitment.id))
    .map((item) => {
      const applicant = findUser(item.applicantUserId)
      return {
        applicationId: item.id,
        applicantUserId: applicant.id,
        applicantNickname: applicant.nickname,
        applicantAvatar: applicant.avatar,
        destination: recruitment.destination,
        startDate: recruitment.startDate,
        days: recruitment.days,
        status: item.status,
        createdAt: item.createdAt
      }
    })

  return {
    id: recruitment.id,
    destination: recruitment.destination,
    startDate: recruitment.startDate,
    days: recruitment.days,
    status: recruitment.status,
    applicationCount: applications.length,
    createdAt: recruitment.createdAt,
    applications
  }
}

export function getMatchRecommendations(payload) {
  return backendFirst({
    url: '/api/matches/recommend',
    method: 'POST',
    data: payload
  }, () => {
    let list = matchRecruitments.filter((item) => item.status === 'open' && Number(item.publisherUserId) !== Number(currentUser.id))

    if (payload.destination) {
      list = list.filter((item) => String(item.destination).toLowerCase().includes(String(payload.destination).toLowerCase()))
    }

    if (payload.startDate) {
      list = list.filter((item) => item.startDate === payload.startDate || !payload.startDate)
    }

    if (payload.days) {
      list = list.filter((item) => Math.abs(Number(item.days) - Number(payload.days)) <= 1)
    }

    if (!list.length) {
      list = matchRecruitments.filter((item) => item.status === 'open' && Number(item.publisherUserId) !== Number(currentUser.id))
    }

    return {
      list: list.map(buildRecommendedCard),
      total: list.length
    }
  }, 480)
}

export function createRecruitment(payload) {
  return backendFirst({
    url: '/api/matches/recruitments',
    method: 'POST',
    data: payload
  }, () => {
    const nextItem = {
      id: getNextRecruitmentId(),
      publisherUserId: currentUser.id,
      destination: payload.destination,
      startDate: payload.startDate,
      days: Number(payload.days),
      status: 'open',
      createdAt: getNowLabel()
    }
    matchRecruitments.unshift(nextItem)
    return buildMyRecruitment(nextItem)
  })
}

export function applyRecruitment(recruitId) {
  return backendFirst({
    url: `/api/matches/recruitments/${recruitId}/apply`,
    method: 'POST'
  }, () => {
    const recruitment = findRecruitment(recruitId)
    if (!recruitment || Number(recruitment.publisherUserId) === Number(currentUser.id)) {
      return {
        applicationId: null,
        status: 'none'
      }
    }

    const existing = getApplicationForCurrentUser(recruitId)
    if (existing) {
      return {
        applicationId: existing.id,
        status: existing.status
      }
    }

    const nextItem = {
      id: getNextApplicationId(),
      recruitId: recruitment.id,
      publisherUserId: recruitment.publisherUserId,
      applicantUserId: currentUser.id,
      status: 'pending',
      createdAt: getNowLabel()
    }
    matchApplications.unshift(nextItem)
    return {
      applicationId: nextItem.id,
      status: nextItem.status
    }
  })
}

export function getMyRecruitments() {
  return backendFirst({
    url: '/api/my/recruitments',
    method: 'GET'
  }, () => ({
    list: matchRecruitments
      .filter((item) => Number(item.publisherUserId) === Number(currentUser.id))
      .map(buildMyRecruitment)
  }))
}

export function getMyRecruitmentDetail(recruitId) {
  return backendFirst({
    url: `/api/my/recruitments/${recruitId}`,
    method: 'GET'
  }, () => buildMyRecruitment(findRecruitment(recruitId)))
}

export function approveRecruitmentApplication(recruitId, applicationId) {
  return backendFirst({
    url: `/api/my/recruitments/${recruitId}/applications/${applicationId}/approve`,
    method: 'POST'
  }, () => {
    const item = matchApplications.find((entry) => Number(entry.id) === Number(applicationId) && Number(entry.recruitId) === Number(recruitId))
    if (item) {
      item.status = 'approved'
    }
    return {
      applicationId: Number(applicationId),
      status: 'approved'
    }
  })
}

export function rejectRecruitmentApplication(recruitId, applicationId) {
  return backendFirst({
    url: `/api/my/recruitments/${recruitId}/applications/${applicationId}/reject`,
    method: 'POST'
  }, () => {
    const item = matchApplications.find((entry) => Number(entry.id) === Number(applicationId) && Number(entry.recruitId) === Number(recruitId))
    if (item) {
      item.status = 'rejected'
    }
    return {
      applicationId: Number(applicationId),
      status: 'rejected'
    }
  })
}

export function getMyMatchApplications() {
  return backendFirst({
    url: '/api/my/match-applications',
    method: 'GET'
  }, () => ({
    list: matchApplications
      .filter((item) => Number(item.applicantUserId) === Number(currentUser.id))
      .map((item) => {
        const recruitment = findRecruitment(item.recruitId)
        const publisher = findUser(item.publisherUserId)
        return {
          applicationId: item.id,
          recruitId: item.recruitId,
          publisherUserId: publisher.id,
          publisherNickname: publisher.nickname,
          publisherAvatar: publisher.avatar,
          destination: recruitment ? recruitment.destination : '',
          startDate: recruitment ? recruitment.startDate : '',
          days: recruitment ? recruitment.days : '',
          status: item.status,
          createdAt: item.createdAt
        }
      })
  }))
}
