import apiClient from '@/services/apiClient';
import type { AxiosResponse } from 'axios';
import type { 
  LoginResponse, 
  CheckSessionResponse, 
  ProfileResponse 
} from '@/types';
import type { SignUpForm } from '@/types'

export const authService = {
  
  // AxiosResponse<LoginResponse> 表示 data 屬性會是 LoginResponse 型別
  login(username: string, password: string): Promise<AxiosResponse<LoginResponse>> {
    return apiClient.post<LoginResponse>('auth/login', { username, password });
  },

  logout(): Promise<AxiosResponse<{ msg: string }>> {
    return apiClient.post('auth/logout');
  },

  checkSession(): Promise<AxiosResponse<CheckSessionResponse>> {
    return apiClient.get<CheckSessionResponse>('auth/check_session');
  },
  
  getProfile(): Promise<AxiosResponse<ProfileResponse>> {
    return apiClient.get<ProfileResponse>('auth/profile');
  },

  signUp(formData: SignUpForm): Promise<AxiosResponse<{ msg: string }>> {
    return apiClient.post('auth/register', formData);
  }
};