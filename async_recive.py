import asyncio
from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage

'''
AbstractIncomingMessage: Это абстрактный тип данных, который
указывает на ожидаемый тип объекта message. В данном случае,
AbstractIncomingMessage является абстрактным базовым классом,
предоставляемым библиотекой aio-pika для представления входящего
сообщения из RabbitMQ.
'''
async def on_message(message: AbstractIncomingMessage) -> None:
    """
    on_message doesn't necessarily have to be defined as async.
    Here it is to show that it's possible.
    """
    print(" [x] Received message %r" % message)
    '''
    В этой строке %r используется для вставки строки, представляющей тело
    сообщения (message.body), вместо %r. Таким образом, в результате
    выполнения этой строки будет выведено сообщение вида
    "Message body is: 'значение_тела_сообщения'",
    где 'значение_тела_сообщения' - это строковое представление
    тела сообщения с использованием repr().
    '''
    print("Message body is: %r" % message.body)

    print("Before sleep!")
    await asyncio.sleep(5)  # Represents async I/O operations
    print("After sleep!")


async def main() -> None:
    '''
    Строка "amqp://guest:guest@localhost/" представляет URL для подключения 
    к серверу RabbitMQ. Давайте разберем его состав:

    amqp: Это протокол, который используется для общения с RabbitMQ. 
    AMQP (Advanced Message Queuing Protocol) является стандартным 
    протоколом для сообщений в архитектуре сообщений.

    guest:guest: Это пара логина и пароля для подключения к RabbitMQ.
    В данном случае используются стандартные учетные данные, где "guest" - это логин, а "guest" - это пароль.

    localhost: Это адрес хоста, где запущен сервер RabbitMQ. 
    В данном случае сервер запущен на том же компьютере, где выполняется код.
    '''
    connection = await connect("amqp://guest:guest@localhost/")
    
    async with connection:
        channel = await connection.channel()
        
        queue = await channel.declare_queue("hello")
        
        # Start listening the queue with name 'hello'
        '''
        В этой строке await queue.consume(on_message, no_ack=True)
        выполняется подписка на очередь RabbitMQ для получения сообщений.
        Давайте рассмотрим, что делает эта строка и как влияет параметр no_ack.

        queue.consume: Этот метод используется для начала прослушивания
        (подписки) на очередь и получения сообщений. Когда сообщение
        появляется в очереди, функция on_message будет вызвана для
        обработки этого сообщения.

        on_message: Это функция, которая будет вызываться для каждого
        полученного сообщения. Вы должны определить эту функцию.
        
        no_ack=True: Это параметр, который указывает, следует ли использовать 
        подтверждение получения (acknowledgment) сообщения. Если no_ack=True,
        то это означает, что сообщение будет автоматически подтверждено
        (acknowledged) системой после того, как функция on_message будет вызвана.
        те RabbitMQ и AMQP, подтверждение (acknowledgment) используется
        для указания того, что сообщение было успешно обработано.
        Если no_ack=True, то система не ожидает подтверждения, 
        что может быть полезным в случаях, когда вы готовы потерять
        сообщение в случае сбоя обработки.
        '''
        await queue.consume(on_message, no_ack=True)
        
        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()
        
if __name__ == "__main__":
    asyncio.run(main())