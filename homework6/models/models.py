from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class TotalRequestsModel(Base):

    __tablename__ = 'Total'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Total: number_of_requests={self.number_of_requests}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number_of_requests = Column(Integer, nullable=False)


class TotalRequestsByTypeModel(Base):

    __tablename__ = 'Total_by_type'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Total_by_type: type_of_request={self.type}, number_of_requests={self.number_of_requests}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(10), nullable=False)
    number_of_requests = Column(Integer, nullable=False)


class MostFrequentRequestsModel(Base):

    __tablename__ = 'Top_frequent_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Top_frequent_requests: url={self.url},  number_of_requests={self.number_of_requests}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(70), nullable=False)
    number_of_requests = Column(Integer, nullable=False)


class LongestRequestsModel(Base):

    __tablename__ = 'Top_5_long_requests_with_code_4XX'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Top_5_long_requests_with_code_4XX: url={self.number_of_requests}, request_size={self.request_size}," \
               f" status_code={self.status_code}, ip={self.ip}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(500), nullable=False)
    request_size = Column(Integer, nullable=False)
    status_code = Column(Integer, nullable=False)
    ip = Column(String(20), nullable=False)


class HighestNumberRequestsIpModel(Base):

    __tablename__ = 'Top_5_IPs_with_highest_number_of_req_code_5XX'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f"<Top_5_IPs_with_highest_number_of_req_code_5XX: ip={self.ip}, " \
               f"number_of_requests={self.number_of_requests}>"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(20), nullable=False)
    number_of_requests = Column(Integer, nullable=False)
