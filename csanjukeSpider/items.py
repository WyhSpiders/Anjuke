# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
  
import scrapy
  
  
class CsanjukespiderItem(scrapy.Item):
  # define the fields for your item here like:
  # name = scrapy.Field()

  # 房子链接
  house_link = scrapy.Field()

  # 房子标题
  long_title = scrapy.Field()
  
  # 安选验真标签 
  c_label = scrapy.Field()
  
  # 房屋图片列表
  #house_pics = scrapy.Field()
  
  # 房屋编号
  num = scrapy.Field()
  
  # 房屋发布时间
  release_time = scrapy.Field()
  
  # 所属小区
  community = scrapy.Field()
  
  # 所在位置
  location = scrapy.Field()
  
  # 建造年代
  built_year = scrapy.Field()
  
  # 房屋类型
  house_type = scrapy.Field()
  
  # 房屋户型
  house_structure = scrapy.Field()
  
  # 建筑面积
  house_space = scrapy.Field()
  
  # 房屋朝向
  house_orientation = scrapy.Field()
  
  # 所在楼层
  house_floor = scrapy.Field()
  
  # 房屋单价
  unit_price = scrapy.Field()
  
  # 参考首付
  down_payment = scrapy.Field()
  
  # 参考月供
  #monthly_payment = scrapy.Field()
  
  # 装修程度
  decoration = scrapy.Field()
  
  # 核心卖点
  house_advantage = scrapy.Field()
  
  # 业主心态
  owner_thought = scrapy.Field()
  
  # 服务佣金
  commission = scrapy.Field()
  
  # 小区配套
  community_supporting = scrapy.Field()
  
  # 小区概况
  community_overview = scrapy.Field()
  
  # 小区户型
  #community_structure = scrapy.Field()
  
  # 小区设施
  #community_facilities = scrapy.Field()
  
  # 小区生活配套
  #residential_facilities = scrapy.Field()
  
  # 小区轨道交通
  #community_transportation = scrapy.Field()
  
  # 小区不足
  community_defects = scrapy.Field()
