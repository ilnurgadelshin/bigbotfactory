from telegram.api.core.api import TelegramAPIHandler
import time


def main():
    batches = 13
    batch_size = 20
    sleep_time = 1

    token = '###'
    api_handler = TelegramAPIHandler(token)
    chat_id = 123456789
    errors_count = 0
    current_time = time.time()
    for i in xrange(batches):
        for j in xrange(batch_size):
            resp = api_handler.send_message(chat_id, 'test')
            if not resp.ok:
                errors_count += 1
            print "Done: ", 100.0 * (i * batch_size + j + 1) / (batch_size * batches), '%'
        time.sleep(sleep_time)

    current_time = time.time() - current_time
    print "Total time: ", current_time
    print "Total errors: ", errors_count
    print "Sending total time: ", current_time - sleep_time * batches
    print "Average time by send message: ", 1.0 * (current_time - sleep_time * batches) / (batches * batch_size)


if __name__ == '__main__':
    main()