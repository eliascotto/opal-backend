import { MonoTypeOperatorFunction, OperatorFunction, SchedulerLike, ValueFromArray } from '../types';
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function startWith<T>(scheduler: SchedulerLike): MonoTypeOperatorFunction<T>;
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function startWith<T, D>(v1: D, scheduler: SchedulerLike): OperatorFunction<T, T | D>;
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function startWith<T, D, E>(v1: D, v2: E, scheduler: SchedulerLike): OperatorFunction<T, T | D | E>;
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function startWith<T, D, E, F>(v1: D, v2: E, v3: F, scheduler: SchedulerLike): OperatorFunction<T, T | D | E | F>;
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function startWith<T, D, E, F, G>(v1: D, v2: E, v3: F, v4: G, scheduler: SchedulerLike): OperatorFunction<T, T | D | E | F | G>;
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function startWith<T, D, E, F, G, H>(v1: D, v2: E, v3: F, v4: G, v5: H, scheduler: SchedulerLike): OperatorFunction<T, T | D | E | F | G | H>;
/** @deprecated The scheduler argument is deprecated, use scheduled and concatAll. Details: https://rxjs.dev/deprecations/scheduler-argument */
export declare function startWith<T, D, E, F, G, H, I>(v1: D, v2: E, v3: F, v4: G, v5: H, v6: I, scheduler: SchedulerLike): OperatorFunction<T, T | D | E | F | G | H | I>;
export declare function startWith<T, A extends any[] = T[]>(...values: A): OperatorFunction<T, T | ValueFromArray<A>>;
//# sourceMappingURL=startWith.d.ts.map