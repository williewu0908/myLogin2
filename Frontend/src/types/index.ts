// 來自 /api/check_session 或 /api/login 的使用者資料
export interface User {
  username: string;
  // 也可以加入 email, id 等
}

// 來自 /api/login 的回應
export interface LoginResponse {
  msg: string;
  user: User;
}

// 來自 /api/check_session 的回應
export interface CheckSessionResponse {
  is_logged_in: boolean;
  user?: User;
}

// 來自 /api/profile 的回應
export interface ProfileResponse {
  logged_in_as: string;
  message: string;
}