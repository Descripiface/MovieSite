from app import app
# from driver.driver_blueprint import driver
# from manager.manage_blueprint import manage

#import view

# # Файл запуска проекта(точка входа)
#
# app.register_blueprint(driver, url_prefix='/driver')
# app.register_blueprint(manage, url_prefix='/manager')

if __name__ == '__main__':
    app.run()
