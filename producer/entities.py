from random import sample, choices, uniform
import string
import pycountry
import pycountry_convert as pc
from pytz import country_timezones, timezone
from datetime import datetime, time

eligible_countries = [x for x in list(pycountry.countries) if x.alpha_2 in [y for y in country_timezones]]

def country_to_continent(country_name):
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name

def create_instrument():
    country = sample(eligible_countries, 1)[0]
    bbg_ticker = ''.join(choices(string.ascii_uppercase, k=3)) + ' ' + country.alpha_2
    return {'date': datetime.utcnow().date(),
            'bbg_id': bbg_ticker,
            'bbg_ticker': bbg_ticker,
            'qid': bbg_ticker,
            'open_time': time(8, 0, 0),
            'country' : country.name,
            'factset_exchange_code': country.alpha_2,
            'close_time': time(16, 30, 0),
            'n_bucket': 510}


def get_condition_codes(instrument):
    
    return [{'bbg_ticker': instrument['bbg_id'], 'country': instrument['country'], 'code': '', 'description': 'normal trading', 'phase': 'continuous'},
            {'bbg_ticker': instrument['bbg_id'],'country': instrument['country'], 'code': 'OA', 'description': 'opening', 'phase': 'opening_auction'},
            {'bbg_ticker': instrument['bbg_id'],'country': instrument['country'], 'code': 'CA', 'description': 'opening', 'phase': 'closing_auction'},
            ]

def create_trade(instrument):
    country = pycountry.countries.get(name=instrument['country'])
    local_time = datetime.now(timezone(country_timezones[country.alpha_2][0]))
    offset = local_time.utcoffset().total_seconds()/60/60
    price = abs(hash(instrument['bbg_id'])) / 1e18 * (1 + uniform(-0.001, 0.001))
    qty = round(uniform(1, 1000))
    drop_mmt = True
    try:
        if country_to_continent(country.name)=="EU":
            drop_mmt = True
    except:
        pass

    dt = datetime.now()
    ret = {'bbgid': instrument['bbg_id'], 'time_zone_number_rt': int(offset), 'mmt_version_rt': 'MMT_V3.04',
             'native_mmt_values_rt': 'Native or ESMA', 'evt_trade_size_rt': qty, 'evt_trade_price_rt': price,
             'evt_trade_time_rt': dt.time().isoformat(), 'evt_trade_datetime': dt.isoformat(), 
             'evt_trade_identifier_rt': '', 'evt_trade_integer_identifier_rt': '',
             'evt_trade_original_identifier_rt': '', 'num_trades_rt': 341, 'EVT_TRD_MMT_LEVL_1_TRD_TYP_CD_RT': '',
             'EVT_TRD_MMT_LEVL_2_TRD_TYP_CD_RT': '', 'EVT_TRD_MMT_LVL_3.1_TRD_T_CD_RT': '',
               'EVT_TRD_MMT_LVL_3.2_TRD_T_CD_RT': '', 'EVT_TRD_MMT_LVL_3.3_TRD_T_CD_RT':'',
               'EVT_TRD_MMT_LVL_3.4_TRD_T_CD_RT': '', 'EVT_TRD_MMT_LVL_3.5_TRD_T_CD_RT':'',
               'EVT_TRD_MMT_LVL_3.6_TRD_T_CD_RT': '', 'EVT_TRD_MMT_LVL_3.7_TRD_T_CD_RT':'',
               'EVT_TRD_MMT_LVL_3.8_TRD_T_CD_RT': '', 'EVT_TRD_MMT_LVL_3.9_TRD_T_CD_RT':'',
               'EVT_TRD_MMT_LEVL_4_TRD_TYP_CD_RT': '', 'EVT_TRD_MMT_LVL_4.1_TRD_T_CD_RT':'',
               'EVT_TRD_MMT_LVL_4.2_TRD_T_CD_RT': '', 'EVT_TRD_MMT_LVL_5_TRD_TYP_CD_RT':'',
               'evt_trade_condition_code_rt': sample(['OA', 'CO', ''], 1)[0], 'evt_trade_indicator_realtime': '',
               'evt_trade_esma_trade_flags_rt': '', 'exch_code_last': '', 'evt_trade_bloomberg_std_cc_rt': '',
               'evt_trade_source_type_code_rt': '', 'evt_trade_mkt_partic_src_tm_rt': '',
               'evt_trade_rpt_prty_side_rt': '', 'evt_trade_bic_rt': '', 'evt_trade_aggressor_rt': 'B',
               'evt_trade_mic_rt': 'XBRU', 'evt_trade_discount_rt': ''}

    if drop_mmt:
        for k in list( ret.keys()):
            if 'mmt' in k.lower():
                del ret[k]

    return ret


def flatten(l):
    return [y for x in l for y in x]

def create_condition_codes(instrument):
    return get_condition_codes(instrument)

# print(create_trade(create_instrument()))
# print(create_condition_codes(create_instrument()))
