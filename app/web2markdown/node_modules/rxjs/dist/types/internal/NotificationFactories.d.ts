import { CompleteNotification, NextNotification, ErrorNotification } from './types';
/**
 * A completion object optimized for memory use and created to be the
 * same "shape" as other notifications in v8.
 * @internal
 */
export declare const COMPLETE_NOTIFICATION: CompleteNotification;
/**
 * Internal use only. Creates an optimized error notification that is the same "shape"
 * as other notifications.
 * @internal
 */
export declare function errorNotification(error: any): ErrorNotification;
/**
 * Internal use only. Creates an optimized next notification that is the same "shape"
 * as other notifications.
 * @internal
 */
export declare function nextNotification<T>(value: T): NextNotification<T>;
/**
 * Ensures that all notifications created internally have the same "shape" in v8.
 *
 * TODO: This is only exported to support a crazy legacy test in `groupBy`.
 * @internal
 */
export declare function createNotification(kind: 'N' | 'E' | 'C', value: any, error: any): {
    kind: "N" | "E" | "C";
    value: any;
    error: any;
};
//# sourceMappingURL=NotificationFactories.d.ts.map