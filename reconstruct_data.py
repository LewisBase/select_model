# -*- coding: utf-8 -*-
"""
@DATE: 2025-03-24 16:10:47
@Author: Liu Hengjiang
@File: reconstruct_data.py
@Software: vscode
@Description:
        重构选型数据表
"""

import pandas as pd
import streamlit as st

from functional import seq


# 定义正确的用户名和密码
USERNAME = "zzd"
PASSWORD = "aini10000nian"


def load_database(excel_file):
    sheets = pd.read_excel(excel_file, sheet_name=None, header=0, index_col=0)

    # 将每个sheet的内容分别保存在不同的DataFrame中
    dataframes = {
        sheet_name: pd.DataFrame(data)
        for sheet_name, data in sheets.items()
    }
    return dataframes


def search_ID_map(mesg: str, dataframes: dict, task: str = "2name"):
    if task == "2name":
        return dataframes["ID_map"].query("编码==@mesg")["含义"].values[0]
    elif task == "2code":
        return dataframes["ID_map"].query("含义==@mesg")["编码"].values[0]
    elif task == "list_code":
        return dataframes["ID_map"].query("项目==@mesg")["编码"].values.tolist()


def generate_model(variables: dict, dataframes: dict):
    if variables["select_ZHDM_option"]:
        select_CS_code = search_ID_map(
            variables["select_CS_option"], dataframes,
            "2code") if variables["select_CS_option"] else ""

        select_PL_code = search_ID_map(
            variables["select_PL_option"], dataframes,
            "2code") if variables["select_PL_option"] else ""
        select_P_code = search_ID_map(
            variables["select_P_option"], dataframes,
            "2code") if variables["select_P_option"] else ""
        select_FLBZ_code = search_ID_map(
            variables["select_FLBZ_option"], dataframes,
            "2code") if variables["select_FLBZ_option"] else ""
        select_Q_code = search_ID_map(
            variables["select_Q_option"], dataframes,
            "2code") if variables["select_Q_option"] else ""
        select_WXTS_code = search_ID_map(
            variables["select_WXTS_option"], dataframes,
            "2code") if variables["select_WXTS_option"] else ""
        select_FLCZ_code = search_ID_map(
            variables["select_FLCZ_option"], dataframes,
            "2code") if variables["select_FLCZ_option"] else ""
        select_W_code = search_ID_map(
            variables["select_W_option"], dataframes,
            "2code") if variables["select_W_option"] else ""
        select_L_code = search_ID_map(
            variables["select_L_option"], dataframes,
            "2code") if variables["select_L_option"] else ""

        select_CLCL_code = search_ID_map(
            variables["select_CLCL_option"], dataframes,
            "2code") if variables["select_CLCL_option"] else ""
        final_model = f"EMF{variables['select_ZHDM_option']}01-({variables['select_KJ_option']})12400{select_CS_code}00{select_PL_code}{select_P_code}{select_FLBZ_code}{select_Q_code}{select_WXTS_code}{select_FLCZ_code}{select_W_code}{select_L_code}"
        return final_model
    else:
        return ""


def generate_DN(variables: dict, dataframes: dict):
    if variables["select_KJ_option"] and variables['select_FLBZ_option']:
        select_KJ_code = search_ID_map(variables["select_KJ_option"],
                                       dataframes, "2code")
        return f"DN{select_KJ_code.split('_')[1]} {variables['select_FLBZ_option']}"
    else:
        return ""
    

# 创建一个函数来验证用户名和密码
def check_password():
    def password_entered():
        if st.session_state["username"] == USERNAME and st.session_state["password"] == PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # 删除密码以防止泄露
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # 用户名输入框
        st.text_input("用户名", key="username")
        # 密码输入框
        st.text_input("密码", type="password", key="password")
        # 登录按钮
        st.button("登录", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("用户名", key="username")
        st.text_input("密码", type="password", key="password")
        st.error("用户名或密码错误")
        st.button("登录", on_click=password_entered)
        return False
    else:
        return True
    
    
def main_func(dataframes, FLBZ_codes, WXTS_codes, FLCZ_codes):
    st.title("电磁流量计选型系统（法兰连接型）")
    st.image("images/开场图.png", use_container_width=True)
    st.title("筛选条件")

    # 所有选项
    variables = {
        "select_JZLX_option": None,
        "select_BCJZ_option": None,
        "select_JZWD_option": None,
        "select_Ex_option": None,
        "select_PL_option": None,
        "select_FHDJ_option": None,
        "select_KJ_option": None,
        "select_GDCZ_option": None,
        "select_P_option": None,
        "select_CLCL_option": None,
        "select_DJCL_option": None,
        "select_JDYJ_option": None,
        "select_CS_option": None,
        "select_GDDY_option": None,
        "select_SCXH_option": None,
        "select_Q_option": None,
        "select_WXTS_option": None,
        "select_ZHDM_option": None,
        "select_FLCZ_option": None,
        "select_W_option": None,
        "select_L_option": None,
        "select_FLBZ_option": None,
    }
    # 主界面布局
    cols = st.columns(3)
    n = 0
    with cols[n%3]:
        with st.container(height=400):
            # step 1. 被测介质类型所有选项
            with st.expander("被测介质类型", expanded=True):
                JZLX_options = seq(dataframes["JZLX"].index).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).list()
                ## step 1.1 进行被测介质类型选择
                variables["select_JZLX_option"] = st.radio("",
                                                           horizontal=True,
                                                           options=JZLX_options,
                                                           index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_JZLX_option"]:
                select_JZLX_code = search_ID_map(variables["select_JZLX_option"],
                                                 dataframes, "2code")
                ## step 1.2 筛选被测介质类型后的有效选项
                valid_options = dataframes["JZLX"][dataframes["JZLX"] == "√"].loc[
                    select_JZLX_code].dropna().index.tolist()
                ### 被测介质有效选项
                BCJZ_options = seq(valid_options).filter(
                    lambda x: x.startswith("BCJZ_")).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                ### 防雷击保护有效选项
                PL_options = seq(valid_options).filter(
                    lambda x: x.startswith("PL")).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                ### 口径有效选项
                KJ_options = seq(valid_options).filter(
                    lambda x: x.startswith("KJ_")).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                # step 2. 进行被测介质选择
                with st.expander("测量介质", expanded=True):
                    variables["select_BCJZ_option"] = st.radio(
                        "", horizontal=True, options=BCJZ_options, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_BCJZ_option"]:
                select_BCJZ_name = search_ID_map(variables["select_BCJZ_option"],
                                                 dataframes, "2code")
                # step 3. 进行介质温度选择
                with st.expander("介质温度", expanded=True):
                    JZWD_options = seq(dataframes["JZWD"].index).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                    variables["select_JZWD_option"] = st.radio(
                        "", horizontal=True, options=JZWD_options, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_JZWD_option"]:
                select_JZWD_code = search_ID_map(variables["select_JZWD_option"],
                                                 dataframes, "2code")
                ## step 3.1 筛选介质温度后的有效选项
                valid_options = dataframes["JZWD"][dataframes["JZWD"] == "√"].loc[
                    select_JZWD_code].dropna().index.tolist()
                ### 流量计结构有效选项
                CS_options_1st = seq(valid_options).filter(lambda x: x.startswith(
                    ("C", "S"))).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                # step 4. 进行是否防爆选择
                with st.expander("是否防爆", expanded=True):
                    Ex_options = seq(dataframes["Ex"].index).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                    variables["select_Ex_option"] = st.radio("",
                                                             horizontal=True,
                                                             options=Ex_options,
                                                             index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            st.markdown('<div class="col">', unsafe_allow_html=True)
            if variables["select_Ex_option"]:
                select_Ex_code = search_ID_map(variables["select_Ex_option"],
                                               dataframes, "2code")
                ## step 4.1 筛选是否防爆后的有效选项
                valid_options = dataframes["Ex"][dataframes["Ex"] == "√"].loc[
                    select_Ex_code].dropna().index.tolist()
                ### 转换代码有效选项
                ZHDM_options_1st = seq(valid_options).filter(
                    lambda x: x.startswith("ZHDM_")).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                ### 电气接口有效选项
                W_options_1st = seq(valid_options).filter(
                    lambda x: x.startswith("W")).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                ### 防护等级有效选项
                FHDJ_options = seq(valid_options).filter(
                    lambda x: x.startswith("FHDJ_")).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                # step 5. 防雷击保护选择
                with st.expander("防雷击保护", expanded=True):
                    variables["select_PL_option"] = st.radio("",
                                                             horizontal=True,
                                                             options=PL_options,
                                                             index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_PL_option"]:
                select_PL_code = search_ID_map(variables["select_PL_option"],
                                               dataframes, "2code")
                ## step 5.1 筛选防雷击保护后的有效选项
                valid_options = dataframes["PL"][dataframes["PL"] == "√"].loc[
                    select_PL_code].dropna().index.tolist()
                ### 转换代码有效选项
                ZHDM_options_2nd = seq(valid_options).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).filter(
                        lambda x: x in ZHDM_options_1st).list()
                ### 供电电源有效选项
                GDDY_options = seq(valid_options).filter(
                    lambda x: x.startswith("GDDY_")).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                # step 6. 防护等级选择
                with st.expander("防护等级", expanded=True):
                    variables["select_FHDJ_option"] = st.radio(
                        "", horizontal=True, options=FHDJ_options, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_FHDJ_option"]:
                select_FHDJ_code = search_ID_map(variables["select_FHDJ_option"],
                                                 dataframes, "2code")
                ## step 6.1 筛选防护等级后的有效选项
                valid_options = dataframes["FHDJ"][dataframes["FHDJ"] == "√"].loc[
                    select_FHDJ_code].dropna().index.tolist()
                ### 流量计结构有效选项
                CS_options_2nd = seq(valid_options).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).filter(
                        lambda x: x in CS_options_1st).list()
                ### 转换代码有效选项
                ZHDM_options_3rd = seq(valid_options).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).filter(
                        lambda x: x in ZHDM_options_2nd).list()
                # step 7. 口径选择
                with st.expander("口径", expanded=True):
                    variables["select_KJ_option"] = st.radio("",
                                                             horizontal=True,
                                                             options=KJ_options,
                                                             index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_KJ_option"]:
                select_KJ_code = search_ID_map(variables["select_KJ_option"],
                                               dataframes, "2code")
                ## step 7.1 筛选口径后的有效选项
                valid_options = dataframes["KJ"][dataframes["KJ"] == "√"].loc[
                    select_KJ_code].dropna().index.tolist()
                ### 耐压等级有效选项
                P_options = seq(valid_options).filter(
                    lambda x: x.startswith("P")).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                ### 接地元件有效选项
                JDYJ_options_1st = seq(valid_options).filter(
                    lambda x: x.startswith("JDYJ_")).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                ### 电极材料有效选项
                DJCL_options_1st = seq(valid_options).filter(
                    lambda x: x.startswith("DJCL_")).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                ### 法兰标准有效选项
                FLBZ_options_1st = seq(valid_options).filter(
                    lambda x: x in FLBZ_codes).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                ### 准确度有效选项
                Q_options_1st = seq(valid_options).filter(
                    lambda x: x.startswith("Q")).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                # step 8. 管道材质选择
                with st.expander("管道材料", expanded=True):
                    GDCZ_options = seq(dataframes["GDCZ"].index).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                    variables["select_GDCZ_option"] = st.radio(
                        "", horizontal=True, options=GDCZ_options, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_GDCZ_option"]:
                select_GDCZ_code = search_ID_map(variables["select_GDCZ_option"],
                                                 dataframes, "2code")
                ## step 8.1 筛选管道材质后的有效选项
                valid_options = dataframes["GDCZ"][dataframes["GDCZ"] == "√"].loc[
                    select_GDCZ_code].dropna().index.tolist()
                ### 电极材料有效选项
                DJCL_options_2nd = seq(valid_options).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).filter(
                        lambda x: x in DJCL_options_1st).list()
                ### 接地元件有效选项
                JDYJ_options_2nd = seq(valid_options).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).filter(
                        lambda x: x in JDYJ_options_1st).list()
                # step 9. 耐压等级选择
                with st.expander("耐压等级", expanded=True):
                    variables["select_P_option"] = st.radio("",
                                                            horizontal=True,
                                                            options=P_options,
                                                            index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_P_option"]:
                select_P_code = search_ID_map(variables["select_P_option"],
                                              dataframes, "2code")
                ## step 9.1 筛选耐压等级后的有效选项
                valid_options = dataframes["P"][dataframes["P"] == "√"].loc[
                    select_P_code].dropna().index.tolist()
                ### 法兰标准有效选项
                FLBZ_options_2nd = seq(valid_options).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).filter(
                        lambda x: x in FLBZ_options_1st).list()
                # step 10. 法兰标准选择
                with st.expander("法兰标准", expanded=True):
                    variables["select_FLBZ_option"] = st.radio(
                        "", horizontal=True, options=FLBZ_options_2nd, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            # step 11. 衬里材料选择
            if variables["select_FLBZ_option"]:
                with st.expander("衬里材料", expanded=True):
                    CLCL_options = seq(dataframes["CLCL"].index).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                    variables["select_CLCL_option"] = st.radio(
                        "", horizontal=True, options=CLCL_options, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_CLCL_option"]:
                select_CLCL_code = search_ID_map(variables["select_CLCL_option"],
                                                 dataframes, "2code")
                ## step 11.1 筛选衬里材料后的有效选项
                valid_options = dataframes["CLCL"][dataframes["CLCL"] == "√"].loc[
                    select_CLCL_code].dropna().index.tolist()
                ### 准确度有效选项
                Q_options_2nd = seq(valid_options).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).filter(
                        lambda x: x in Q_options_1st).list()
                ### 电极材料有效选项
                DJCL_options_3rd = seq(valid_options).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).filter(
                        lambda x: x in DJCL_options_2nd).list()
                # step 12. 电极材料选择
                with st.expander("电极材料", expanded=True):
                    variables["select_DJCL_option"] = st.radio(
                        "", horizontal=True, options=DJCL_options_3rd, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            # step 13. 接地元件选择
            if variables["select_DJCL_option"]:
                with st.expander("接地元件", expanded=True):
                    variables["select_JDYJ_option"] = st.radio(
                        "", horizontal=True, options=JDYJ_options_2nd, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            # step 14. 流量计结构选择
            if variables["select_JDYJ_option"]:
                with st.expander("流量计结构", expanded=True):
                    variables["select_CS_option"] = st.radio(
                        "", horizontal=True, options=CS_options_2nd, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_CS_option"]:
                select_CS_code = search_ID_map(variables["select_CS_option"],
                                               dataframes, "2code")
                ## step 14.1 筛选流量计结构后的有效选项
                valid_options = dataframes["CS"][dataframes["CS"] == "√"].loc[
                    select_CS_code].dropna().index.tolist()
                ### 分体式信号线长度有效选项
                L_options = seq(valid_options).filter(
                    lambda x: x.startswith("L")).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                ### 转换代码有效选项
                ZHDM_options_4th = seq(valid_options).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).filter(
                        lambda x: x in ZHDM_options_3rd).list()

                # step 15. 供电电源选择
                with st.expander("供电电源", expanded=True):
                    variables["select_GDDY_option"] = st.radio(
                        "", horizontal=True, options=GDDY_options, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_GDDY_option"]:
                select_GDDY_code = search_ID_map(variables["select_GDDY_option"],
                                                 dataframes, "2code")
                ## step 15.1 筛选供电电源后的有效选项
                valid_options = dataframes["GDDY"][dataframes["GDDY"] == "√"].loc[
                    select_GDDY_code].dropna().index.tolist()
                ### 转换代码有效选项
                ZHDM_options_5th = seq(valid_options).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).filter(
                        lambda x: x in ZHDM_options_4th).list()
                # step 16. 输出信号选择
                with st.expander("输出信号", expanded=True):
                    SCXH_options = seq(dataframes["SCXH"].index).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                    variables["select_SCXH_option"] = st.radio(
                        "", horizontal=True, options=SCXH_options, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_SCXH_option"]:
                select_SCXH_code = search_ID_map(variables["select_SCXH_option"],
                                                 dataframes, "2code")
                ## step 16.1 筛选输出信号后的有效选项
                valid_options = dataframes["SCXH"][dataframes["SCXH"] == "√"].loc[
                    select_SCXH_code].dropna().index.tolist()
                ### 转换代码有效选项
                ZHDM_options_6th = seq(valid_options).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).filter(
                        lambda x: x in ZHDM_options_5th).list()
                # step 17. 准确度选择
                with st.expander("准确度", expanded=True):
                    variables["select_Q_option"] = st.radio("",
                                                            horizontal=True,
                                                            options=Q_options_2nd,
                                                            index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_Q_option"]:
                select_Q_code = search_ID_map(variables["select_Q_option"],
                                              dataframes, "2code")
                ## step 17.1 筛选准确度后的有效选项
                valid_options = dataframes["Q"][dataframes["Q"] == "√"].loc[
                    select_Q_code].dropna().index.tolist()
                ### 转换代码有效选项
                ZHDM_options_7th = seq(valid_options).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).filter(
                        lambda x: x in ZHDM_options_6th).list()
                # step 18. 无线通讯方式选择
                with st.expander("无线通讯方式", expanded=True):
                    WXTS_options = seq(WXTS_codes).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                    variables["select_WXTS_option"] = st.radio(
                        "", horizontal=True, options=WXTS_options, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            # step 19. 转换器代码选择
            if variables["select_WXTS_option"]:
                with st.expander("转换器代码", expanded=True):
                    variables["select_ZHDM_option"] = st.radio(
                        "", horizontal=True, options=ZHDM_options_7th, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            if variables["select_ZHDM_option"]:
                select_ZHDM_code = search_ID_map(variables["select_ZHDM_option"],
                                                 dataframes, "2code")
                ## step 19.1 筛选转换器代码后的有效选项
                valid_options = dataframes["ZHDM"][dataframes["ZHDM"] == "√"].loc[
                    select_ZHDM_code].dropna().index.tolist()
                ### 电气接口有效选项
                W_options_2nd = seq(valid_options).map(
                    lambda x: search_ID_map(x, dataframes, "2name")).filter(
                        lambda x: x in W_options_1st).list()
                # step 20. 法兰材质选择
                with st.expander("法兰材质", expanded=True):
                    FLCZ_options = seq(FLCZ_codes).map(
                        lambda x: search_ID_map(x, dataframes, "2name")).list()
                    variables["select_FLCZ_option"] = st.radio(
                        "", horizontal=True, options=FLCZ_options, index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            # step 21. 电气接口选择
            if variables["select_FLCZ_option"]:
                with st.expander("电气接口", expanded=True):
                    variables["select_W_option"] = st.radio("",
                                                            horizontal=True,
                                                            options=W_options_2nd,
                                                            index=None)
        n += 1

    with cols[n%3]:
        with st.container(height=400):
            # step 22. 分体式信号线长度选择
            if variables["select_W_option"]:
                with st.expander("分体式信号线长度", expanded=True):
                    variables["select_L_option"] = st.radio("",
                                                            horizontal=True,
                                                            options=L_options,
                                                            index=None)
        n += 1

    with st.sidebar:
        st.header("选型结果")
        final_model = generate_model(variables, dataframes)
        st.markdown(f"**产品型号：<span style='color:blue'>{final_model}</span>**",
                    unsafe_allow_html=True)
        st.markdown(
            f"**测量介质：<span style='color:blue'>{variables['select_BCJZ_option'] or ''}</span>**",
            unsafe_allow_html=True)
        DN = generate_DN(variables, dataframes)
        st.markdown(
            f"**过程连接：<span style='color:blue'>{DN}</span>**",
            unsafe_allow_html=True)
        st.markdown(
            f"**电极材料：<span style='color:blue'>{variables['select_DJCL_option'] or ''}</span>**",
            unsafe_allow_html=True)
        st.markdown(
            f"**衬里材料：<span style='color:blue'>{variables['select_CLCL_option'] or ''}</span>**",
            unsafe_allow_html=True)
        st.markdown(
            f"**测量介质温度范围：<span style='color:blue'>{variables['select_JZWD_option'] or ''}</span>**",
            unsafe_allow_html=True)
        st.markdown(
            f"**接地元件：<span style='color:blue'>{variables['select_JDYJ_option'] or ''}</span>**",
            unsafe_allow_html=True)
        st.markdown(
            f"**准确度：<span style='color:blue'>{variables['select_Q_option'] or ''}</span>**",
            unsafe_allow_html=True)
        st.markdown(
            f"**供电电源：<span style='color:blue'>{variables['select_GDDY_option'] or ''}</span>**",
            unsafe_allow_html=True)
        st.markdown(
            f"**输出信号：<span style='color:blue'>{variables['select_SCXH_option'] or ''}</span>**",
            unsafe_allow_html=True)
        st.markdown(
            f"**防护等级：<span style='color:blue'>{variables['select_FHDJ_option'] or ''}</span>**",
            unsafe_allow_html=True)
        st.markdown(
            f"**流量计结构：<span style='color:blue'>{variables['select_CS_option'] or ''}</span>**",
            unsafe_allow_html=True)
        st.markdown(
            f"**传感器耐压等级：<span style='color:blue'>{variables['select_P_option'] or ''}</span>**",
            unsafe_allow_html=True)
        st.markdown(
            f"**无线通讯方式：<span style='color:blue'>{variables['select_WXTS_option'] or ''}</span>**",
            unsafe_allow_html=True)
        st.markdown(
            f"**法兰材质：<span style='color:blue'>{variables['select_FLCZ_option'] or ''}</span>**",
            unsafe_allow_html=True)
        st.markdown(
            f"**分体式信号线长度：<span style='color:blue'>{variables['select_L_option'] or ''}</span>**",
            unsafe_allow_html=True)


if __name__ == "__main__":

    excel_file = "database/zzd_original_data.xlsx"
    dataframes = load_database(excel_file)
    FLBZ_codes = search_ID_map("法兰标准", dataframes, "list_code")
    WXTS_codes = search_ID_map("无线通讯方式", dataframes, "list_code")
    FLCZ_codes = search_ID_map("法兰材质", dataframes, "list_code")

    # 开场图
    if check_password():
        main_func(dataframes, FLBZ_codes, WXTS_codes, FLCZ_codes)
