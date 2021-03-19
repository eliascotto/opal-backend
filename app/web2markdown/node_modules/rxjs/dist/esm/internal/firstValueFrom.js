import { EmptyError } from './util/EmptyError';
import { SafeSubscriber } from './Subscriber';
export function firstValueFrom(source) {
    return new Promise((resolve, reject) => {
        const subscriber = new SafeSubscriber({
            next: value => {
                resolve(value);
                subscriber.unsubscribe();
            },
            error: reject,
            complete: () => {
                reject(new EmptyError());
            },
        });
        source.subscribe(subscriber);
    });
}
//# sourceMappingURL=firstValueFrom.js.map