import { mockData } from "../data/userData"

const fetchUser = (email, password) => {
    const userData = mockData.filter(item => item.personal_details?.email === email && item.personal_details?.password === password)
    const user = {
        id: userData?.[0]?.personal_details.id,
        status: userData?.length > 0 ? true : false
    }
    return user;


}
const fetchUserById = (id) => {
    const userData = mockData.filter(item => item.personal_details?.id == id)

    return userData;


}

export { fetchUser, fetchUserById }