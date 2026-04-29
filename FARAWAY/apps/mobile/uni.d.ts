declare const uni: any;

declare function getCurrentPages(): any[];

declare module "@dcloudio/uni-app" {
  export function onLaunch(callback: () => void): void;
  export function onShow(callback: () => void): void;
  export function onHide(callback: () => void): void;
  export function onLoad(callback: (options?: Record<string, string>) => void | Promise<void>): void;
  export function onPullDownRefresh(callback: () => void | Promise<void>): void;
}
