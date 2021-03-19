import { EmptyError } from './util/EmptyError';
import { SafeSubscriber } from './Subscriber';
export function firstValueFrom(source) {
    return new Promise(function (resolve, reject) {
        var subscriber = new SafeSubscriber({
            next: function (value) {
                resolve(value);
                subscriber.unsubscribe();
            },
            error: reject,
            complete: function () {
                reject(new EmptyError());
            },
        });
        source.subscribe(subscriber);
    });
}
//# sourceMappingURL=firstValueFrom.js.map