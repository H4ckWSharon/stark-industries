"""
STARK INDUSTRIES SQL — Platform Configuration
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "STARK INDUSTRIES SQL"
    debug: bool = False
    environment: str = "development"

    # Database (Platform)
    database_url: str = "postgresql://stark_user:stark_db_password_lab@postgres-platform:5432/stark_platform"

    # Redis
    redis_url: str = "redis://redis:6379/0"

    # JWT
    jwt_secret_key: str = "super_secret_jwt_key_change_me_in_production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480

    # Classroom Auth
    classroom_username: str = "stark_student"
    classroom_password: str = "IronMan2025!Lab"
    admin_username: str = "stark_admin"
    admin_password: str = "Jarvis@AdminPanel99"

    # Flags (loaded from env)
    flag_ch01: str = "STARKSQL{basic_injection_r3d_t3am}"
    flag_ch02: str = "STARKSQL{auth_bypass_t0ny_st4rk}"
    flag_ch03: str = "STARKSQL{err0r_based_exfil}"
    flag_ch04: str = "STARKSQL{un10n_m4st3r_s3l3ct}"
    flag_ch05: str = "STARKSQL{bl1nd_b00l_hunt3r}"
    flag_ch06: str = "STARKSQL{t1m3_blind_d3t3ctiv3}"
    flag_ch07: str = "STARKSQL{00b_callb4ck_m4st3r}"
    flag_ch08: str = "STARKSQL{s3c0nd_0rd3r_str1k3}"
    flag_ch09: str = "STARKSQL{st4ck3d_qu3ry_ch4in}"
    flag_ch10: str = "STARKSQL{st0r3d_pr0c_byp4ss}"
    flag_ch11: str = "STARKSQL{1ns3rt_1nj3ct10n}"
    flag_ch12: str = "STARKSQL{upd4t3_byp4ss_pr0}"
    flag_ch13: str = "STARKSQL{d3l3t3_sqli_b00m}"
    flag_ch14: str = "STARKSQL{0rd3r_by_m4n1pul4t10n}"
    flag_ch15: str = "STARKSQL{wh3r3_cl4us3_br34k3r}"
    flag_ch16: str = "STARKSQL{l1k3_cl4us3_byp4ss}"
    flag_ch17: str = "STARKSQL{num3r1c_1nj3ct10n_ftw}"
    flag_ch18: str = "STARKSQL{str1ng_sqli_m4st3r}"
    flag_ch19: str = "STARKSQL{j50n_4p1_pwn3d}"
    flag_ch20: str = "STARKSQL{h34d3r_1nj3ct10n_xpl0it}"
    flag_ch21: str = "STARKSQL{c00ki3_m0nst3r_sqli}"
    flag_ch22: str = "STARKSQL{hpp_p4r4m_p0llut10n}"
    flag_ch23: str = "STARKSQL{w4f_byp4ss_surv1v0r}"
    flag_ch24: str = "STARKSQL{f1lt3r_byp4ss_h4x0r}"
    flag_ch25: str = "STARKSQL{s3c0nd_0rd3r_4uth_pwn}"
    flag_ch26: str = "STARKSQL{mult1_db_3xpl0r3r}"
    flag_ch27: str = "STARKSQL{sql1t3_sp3c14l1st}"
    flag_ch28: str = "STARKSQL{mysql_d33p_d1v3}"
    flag_ch29: str = "STARKSQL{p0stgr3sql_m4st3r}"
    flag_ch30: str = "STARKSQL{mssql_pwn4g3}"

    # Challenge ports
    ch01_port: int = 8001
    ch02_port: int = 8002
    ch03_port: int = 8003
    ch04_port: int = 8004
    ch05_port: int = 8005
    ch06_port: int = 8006
    ch07_port: int = 8007
    ch08_port: int = 8008
    ch09_port: int = 8009
    ch10_port: int = 8010
    ch11_port: int = 8011
    ch12_port: int = 8012
    ch13_port: int = 8013
    ch14_port: int = 8014
    ch15_port: int = 8015
    ch16_port: int = 8016
    ch17_port: int = 8017
    ch18_port: int = 8018
    ch19_port: int = 8019
    ch20_port: int = 8020
    ch21_port: int = 8021
    ch22_port: int = 8022
    ch23_port: int = 8023
    ch24_port: int = 8024
    ch25_port: int = 8025
    ch26_port: int = 8026
    ch27_port: int = 8027
    ch28_port: int = 8028
    ch29_port: int = 8029
    ch30_port: int = 8030

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
