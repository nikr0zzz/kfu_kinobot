from aiogram.utils import executor
from bot import dp
import handlers



if  __name__ == '__main__':
    executor.start_polling(dp)