import logging
import traceback

def catch_exception(except_func):
    def func(*args,**kwargs):

        try:
            return except_func(*args,**kwargs)
        except Exception as e:
            # print('发生错误的文件：', e.__traceback__.tb_frame.f_globals['__file__'])
            # print('错误所在的行号：', e.__traceback__.tb_lineno)

            logging.error(traceback.format_exc())
            print('错误信息', e, )

    return func
