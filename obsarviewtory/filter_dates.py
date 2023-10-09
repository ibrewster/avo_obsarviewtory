# scenes to be ignored, usually due to shifted frames or bad coherence
# if a volcano has no bad scenes then this filter_dates list will be empty
# currently we are defining one filter_dates list for each volcano that needs it

# These scenes will be downloaded, as they may be valid for
# a different volcano. However, they will not be used when
# processing the specified volcano and path
# Dictionary Key is the volc_name, path tuple.
filter_dates = {
    ('seguam', 15): [
        "S1AA_20160422T173706_20160516T173708_VVP024_INT80_G_weF_60A3",
        "S1AA_20160422T173734_20160516T173735_VVP024_INT80_G_weF_540A",
        "S1AA_20160422T173706_20160609T173709_VVP048_INT80_G_weF_CFF3",
        "S1AA_20160422T173734_20160609T173736_VVP048_INT80_G_weF_678B",
        "S1AA_20160516T173708_20160609T173709_VVP024_INT80_G_weF_F0DE",
        "S1AA_20160516T173735_20160609T173736_VVP024_INT80_G_weF_9ED0",
        "S1AA_20160516T173708_20160703T173710_VVP048_INT80_G_weF_06A5",
        "S1AA_20160516T173735_20160703T173738_VVP048_INT80_G_weF_4B9A",
        "S1AA_20160609T173709_20170628T173721_VVP384_INT80_G_weF_7D72",
        "S1AA_20160609T173709_20160703T173710_VVP024_INT80_G_weF_58F4",
        "S1AA_20160609T173736_20160703T173738_VVP024_INT80_G_weF_AB20",
        "S1AA_20160609T173709_20160727T173712_VVP048_INT80_G_weF_91C0",
        "S1AA_20160609T173736_20160727T173739_VVP048_INT80_G_weF_760D",
        "S1AA_20160703T173710_20160727T173712_VVP024_INT80_G_weF_2946",
        "S1AA_20160703T173738_20160727T173739_VVP024_INT80_G_weF_C90D",
        "S1AA_20160703T173710_20160820T173713_VVP048_INT80_G_weF_A3A1",
        "S1AA_20160703T173738_20160820T173741_VVP048_INT80_G_weF_2A83",
        "S1AA_20160727T173712_20160820T173713_VVP024_INT80_G_weF_726F",
        "S1AA_20160727T173739_20160820T173741_VVP024_INT80_G_weF_63BA",
        "S1AA_20160727T173739_20160913T173741_VVP048_INT80_G_weF_9454",
        "S1AA_20160727T173712_20160913T173714_VVP048_INT80_G_weF_47E5",
        "S1AA_20160820T173713_20160913T173714_VVP024_INT80_G_weF_0546",
        "S1AA_20160820T173741_20160913T173741_VVP024_INT80_G_weF_56D9",
        "S1AA_20160820T173713_20170803T173723_VVP348_INT80_G_weF_23B0",
        "S1AB_20160913T173741_20161013T173638_VVP030_INT80_G_weF_5E45",
        "S1AB_20160913T173714_20161013T173638_VVP030_INT80_G_weF_D66A",
        "S1BB_20161013T173638_20161106T173638_VVP024_INT80_G_weF_B9C9"
    ],

    ('kiska', 30): [
        "S1AA_20180624T181853_20180811T181855_VVP048_INT80_G_ueF_219B",
        "S1AA_20180706T181853_20180811T181855_VVP036_INT80_G_ueF_0CA3",
        "S1AA_20180718T181854_20180811T181855_VVP024_INT80_G_ueF_5F24",
        "S1AA_20180730T181855_20180811T181855_VVP012_INT80_G_ueF_C483",
        "S1AA_20180811T181855_20180823T181856_VVP012_INT80_G_ueF_D95E",
        "S1AA_20180811T181855_20180904T181857_VVP024_INT80_G_ueF_56A1",
        "S1AA_20180811T181855_20180916T181857_VVP036_INT80_G_ueF_2E1B",
        "S1AA_20180811T181855_20180928T181857_VVP048_INT80_G_ueF_B216"
    ],

    ('akutan', 44): [
        "S1AA_20181104T172032_20181116T172032_VVP012_INT80_G_weF_F5C6",
        "S1AB_20160915T172019_20161015T171938_VVP030_INT80_G_weF_55A6",
        "S1BB_20161015T171938_20161108T171937_VVP024_INT80_G_weF_3EFB",
    ],

    ('okmok', 44): [
        'S1AA_20160424T172039_20160518T172040_VVP024_INT80_G_weF_ED6C',
        'S1AA_20160424T172039_20160611T172042_VVP048_INT80_G_weF_521D',
        'S1AA_20160518T172040_20160611T172042_VVP024_INT80_G_weF_0A92',
        'S1AA_20160518T172040_20160705T172043_VVP048_INT80_G_weF_3A48',
        'S1AA_20170525T172046_20180508T172052_VVP348_INT80_G_weF_3107',
        'S1AA_20170606T172047_20170618T172048_VVP012_INT80_G_weF_1DE0',
        'S1AA_20171028T172053_20181104T172100_VVP372_INT80_G_weF_F1D3',
        'S1AA_20171121T172053_20181116T172059_VVP360_INT80_G_weF_87BA',
        'S1AA_20180309T172050_20180321T172050_VVP012_INT80_G_weF_6B46',
        'S1AA_20180309T172050_20180402T172050_VVP024_INT80_G_weF_6F6F',
        'S1AA_20180309T172050_20180414T172051_VVP036_INT80_G_weF_3982',
        'S1AA_20180309T172050_20180426T172051_VVP048_INT80_G_weF_BCEF',
        'S1AA_20180321T172050_20180402T172050_VVP012_INT80_G_weF_543C',
        'S1AA_20180321T172050_20180414T172051_VVP024_INT80_G_weF_24AE',
        'S1AA_20180321T172050_20180426T172051_VVP036_INT80_G_weF_C1A3',
        'S1AA_20180321T172050_20180508T172052_VVP048_INT80_G_weF_1C8A',
        'S1AA_20180321T172050_20190316T172056_VVP360_INT80_G_weF_1B34',
        'S1AA_20180426T172051_20190421T172057_VVP360_INT80_G_weF_065D',
        'S1AA_20181116T172059_20191123T172106_VVP372_INT80_G_weF_E3B5',
        'S1AA_20190304T172056_20190316T172056_VVP012_INT80_G_weF_B218',
        'S1AA_20190304T172056_20200322T172103_VVP384_INT80_G_weF_7DAD',
        'S1AA_20190316T172056_20190328T172057_VVP012_INT80_G_weF_F749',
        'S1AA_20190316T172056_20190409T172057_VVP024_INT80_G_weF_F7F6',
        'S1AA_20190316T172056_20190421T172057_VVP036_INT80_G_weF_BEA7',
        'S1AA_20190316T172056_20190503T172058_VVP048_INT80_G_weF_FF7C',
        'S1AA_20191006T172106_20191123T172106_VVP048_INT80_G_weF_13B0',
        'S1AA_20191018T172106_20191123T172106_VVP036_INT80_G_weF_5264',
        'S1AA_20200310T172103_20200322T172103_VVP012_INT80_G_weF_E235',
        'S1AA_20200310T172103_20200403T172103_VVP024_INT80_G_weF_9943',
        'S1AA_20200310T172103_20200415T172103_VVP036_INT80_G_weF_3543',
        'S1AA_20200310T172103_20200427T172104_VVP048_INT80_G_weF_0751',
        'S1AA_20200403T172103_20210422T172110_VVP384_INT80_G_weF_6784',
        'S1AA_20201105T172112_20201117T172112_VVP012_INT80_G_weF_13DC',
        'S1AA_20210305T172108_20210317T172108_VVP012_INT80_G_weF_5F0B',
        'S1AA_20210305T172108_20210329T172109_VVP024_INT80_G_weF_A3DA',
        'S1AA_20210305T172108_20210410T172109_VVP036_INT80_G_weF_0DD1',
        'S1AA_20210305T172108_20210422T172110_VVP048_INT80_G_weF_7F55',
        'S1AA_20210317T172108_20210329T172109_VVP012_INT80_G_weF_BE93',
        'S1AA_20210317T172108_20210410T172109_VVP024_INT80_G_weF_5295',
        'S1AA_20210317T172108_20210422T172110_VVP036_INT80_G_weF_1A8B',
        'S1AA_20210317T172108_20210504T172110_VVP048_INT80_G_weF_EF49',
        'S1AA_20210516T172111_20220405T172115_VVP324_INT80_G_weF_2721',
        'S1AA_20210913T172118_20211031T172118_VVP048_INT80_G_weF_BB6F',
        'S1AA_20210925T172118_20211031T172118_VVP036_INT80_G_weF_4514',
        'S1AA_20210925T172118_20211112T172118_VVP048_INT80_G_weF_F4B5',
        'S1AA_20210925T172118_20221002T172124_VVP372_INT80_G_weF_C2DE',
        'S1AA_20211007T172118_20211031T172118_VVP024_INT80_G_weF_CD06',
        'S1AA_20211007T172118_20211112T172118_VVP036_INT80_G_weF_3DA1',
        'S1AA_20211007T172118_20211124T172118_VVP048_INT80_G_weF_017E',
        'S1AA_20211019T172118_20211031T172118_VVP012_INT80_G_weF_837A',
        'S1AA_20211019T172118_20211112T172118_VVP024_INT80_G_weF_4B4A',
        'S1AA_20211019T172118_20211124T172118_VVP036_INT80_G_weF_D151',
        'S1AA_20211031T172118_20211112T172118_VVP012_INT80_G_weF_1832',
        'S1AA_20211031T172118_20211124T172118_VVP024_INT80_G_weF_6B16',
        'S1AA_20211112T172118_20211124T172118_VVP012_INT80_G_weF_219F',
        'S1AA_20220312T172114_20220324T172114_VVP012_INT80_G_weF_A462',
        'S1AA_20220312T172114_20220405T172115_VVP024_INT80_G_weF_AA64',
        'S1AA_20220312T172114_20220417T172115_VVP036_INT80_G_weF_B7A3',
        'S1AA_20220312T172114_20220429T172116_VVP048_INT80_G_weF_F60B',
        'S1AA_20220324T172114_20220405T172115_VVP012_INT80_G_weF_4CBC',
        'S1AA_20220324T172114_20220417T172115_VVP024_INT80_G_weF_5AB4',
        'S1AA_20220324T172114_20220429T172116_VVP036_INT80_G_weF_C273',
        'S1AA_20220405T172115_20220417T172115_VVP012_INT80_G_weF_08B1',
        'S1AA_20220405T172115_20220429T172116_VVP024_INT80_G_weF_D256',
        'S1AA_20220417T172115_20220429T172116_VVP012_INT80_G_weF_7258',
        'S1AA_20220429T172116_20220616T172119_VVP048_INT80_G_weF_F749',
        'S1AA_20220429T172116_20220827T172123_VVP120_INT80_G_weF_AD63'
    ],

    ('edgecumbe', 50): [
        'S1AA_20230719T170441_20230731T170442_VVR012_INT80_G_weF_B020',
        'S1AA_20220817T170438_20230731T170442_VVR348_INT80_G_weF_6563'
    ],

    ('takawangha', 59): [
        "S1AA_20171005T180224_20181012T180231_VVP372_INT80_G_weF_9A18",
        "S1AA_20180322T180221_20180930T180230_VVP192_INT80_G_weF_A509",
        "S1AA_20180906T180230_20180930T180230_VVP024_INT80_G_weF_98B9",
        "S1AA_20180906T180230_20181012T180231_VVP036_INT80_G_weF_5307",
        "S1AA_20180906T180230_20181024T180231_VVP048_INT80_G_weF_AA15",
        "S1AA_20180918T180230_20180930T180230_VVP012_INT80_G_weF_852A",
        "S1AA_20180918T180230_20181012T180231_VVP024_INT80_G_weF_9079",
        "S1AA_20180918T180230_20181024T180231_VVP036_INT80_G_weF_0939",
        "S1AA_20181024T180231_20191031T180237_VVP372_INT80_G_weF_2AD5",
        "S1AA_20181105T180230_20181129T180230_VVP024_INT80_G_weF_2D20",
        "S1AA_20181117T180230_20181129T180230_VVP012_INT80_G_weF_3A87"
    ],

    ('kanaga', 59): [
        "S1AA_20171005T180224_20181012T180231_VVP372_INT80_G_weF_9A18",
        "S1AA_20180322T180221_20180930T180230_VVP192_INT80_G_weF_A509",
        "S1AA_20180906T180230_20180930T180230_VVP024_INT80_G_weF_98B9",
        "S1AA_20180906T180230_20181012T180231_VVP036_INT80_G_weF_5307",
        "S1AA_20180906T180230_20181024T180231_VVP048_INT80_G_weF_AA15",
        "S1AA_20180918T180230_20180930T180230_VVP012_INT80_G_weF_852A",
        "S1AA_20180918T180230_20181012T180231_VVP024_INT80_G_weF_9079",
        "S1AA_20180918T180230_20181024T180231_VVP036_INT80_G_weF_0939",
        "S1AA_20181024T180231_20191031T180237_VVP372_INT80_G_weF_2AD5",
        "S1AA_20181105T180230_20181129T180230_VVP024_INT80_G_weF_2D20",
        "S1AA_20181117T180230_20181129T180230_VVP012_INT80_G_weF_3A87"
    ],

    ('amak', 73): [
        "S1AA_20141010T170317_20141103T170318_VVP024_INT80_G_weF_CA5D",
        "S1AA_20141010T170317_20141127T170317_VVP048_INT80_G_weF_06B8",
        "S1AA_20141103T170318_20141127T170317_VVP024_INT80_G_weF_0748",
        "S1AA_20150315T170315_20150408T170315_VVP024_INT80_G_weF_CFDE",
        "S1AA_20150315T170315_20150502T170317_VVP048_INT80_G_weF_7334",
        "S1AA_20150408T170315_20150502T170317_VVP024_INT80_G_weF_1CF3",
        "S1AA_20150408T170315_20150526T170318_VVP048_INT80_G_weF_7713",
        "S1AA_20150502T170317_20150526T170318_VVP024_INT80_G_weF_50F5",
        "S1AA_20150502T170317_20150619T170320_VVP048_INT80_G_weF_8637",
        "S1AA_20150526T170318_20150619T170320_VVP024_INT80_G_weF_3040",
        "S1AA_20150526T170318_20150713T170320_VVP048_INT80_G_weF_39B4",
        "S1AA_20150526T170318_20160613T170340_VVP384_INT80_G_weF_022D",
        "S1AA_20150619T170320_20150713T170320_VVP024_INT80_G_weF_C59B",
        "S1AA_20150619T170320_20150806T170322_VVP048_INT80_G_weF_238F",
        "S1AA_20150713T170320_20150806T170322_VVP024_INT80_G_weF_96BC",
        "S1AA_20150713T170320_20150830T170340_VVP048_INT80_G_weF_5051",
        "S1AA_20150806T170322_20150830T170340_VVP024_INT80_G_weF_5128",
        "S1AA_20150806T170322_20150923T170341_VVP048_INT80_G_weF_BC61"
    ],

    ('pavlof', 73): [
        "S1AA_20141010T170317_20141103T170318_VVP024_INT80_G_weF_CA5D",
        "S1AA_20141010T170317_20141127T170317_VVP048_INT80_G_weF_06B8",
        "S1AA_20141103T170318_20141127T170317_VVP024_INT80_G_weF_0748",
        "S1AB_20141127T170317_20161017T170247_VVP690_INT80_G_weF_65BF",
        "S1AA_20150315T170315_20150408T170315_VVP024_INT80_G_weF_CFDE",
        "S1AA_20150315T170315_20150502T170317_VVP048_INT80_G_weF_7334",
        "S1AA_20150408T170315_20150526T170318_VVP048_INT80_G_weF_7713",
        "S1AA_20150408T170315_20150502T170317_VVP024_INT80_G_weF_1CF3",
        "S1AA_20150502T170317_20150526T170318_VVP024_INT80_G_weF_50F5",
        "S1AA_20150502T170317_20150619T170320_VVP048_INT80_G_weF_8637",
        "S1AA_20150526T170318_20150619T170320_VVP024_INT80_G_weF_3040",
        "S1AA_20150526T170318_20150713T170320_VVP048_INT80_G_weF_39B4",
        "S1AA_20150526T170318_20160613T170340_VVP384_INT80_G_weF_022D",
        "S1AA_20150619T170320_20150713T170320_VVP024_INT80_G_weF_C59B",
        "S1AA_20150619T170320_20150806T170322_VVP048_INT80_G_weF_238F",
        "S1AA_20150713T170320_20150806T170322_VVP024_INT80_G_weF_96BC",
        "S1AA_20150713T170320_20150830T170340_VVP048_INT80_G_weF_5051",
        "S1AA_20150806T170322_20150830T170340_VVP024_INT80_G_weF_5128",
        "S1AA_20150806T170322_20150923T170341_VVP048_INT80_G_weF_BC61",
        "S1AA_20150830T170340_20150923T170341_VVP024_INT80_G_weF_91A2",
        "S1AA_20150830T170340_20151017T170341_VVP048_INT80_G_weF_9FC3",
        "S1AA_20150830T170340_20160824T170344_VVP360_INT80_G_weF_76B6",
        "S1AA_20150923T170341_20151017T170341_VVP024_INT80_G_weF_37DE",
        "S1AA_20150923T170341_20151110T170341_VVP048_INT80_G_weF_120B",
        "S1AA_20151017T170341_20151110T170341_VVP024_INT80_G_weF_97B4",
        "S1AB_20160917T170345_20161017T170247_VVP030_INT80_G_weF_9FD6",
        "S1BA_20161017T170247_20181106T170350_VVP750_INT80_G_weF_669E"
    ],

    ('unimak', 73): [
        "S1AA_20150408T170343_20150502T170345_VVP024_INT80_G_weF_4DE3",
        "S1AA_20150713T170348_20150806T170349_VVP024_INT80_G_weF_71B1",
        "S1AA_20150408T170343_20150526T170346_VVP048_INT80_G_weF_017C",
        "S1AA_20150713T170348_20150830T170340_VVP048_INT80_G_weF_00D0",
        "S1AA_20150502T170345_20150526T170346_VVP024_INT80_G_weF_1332",
        "S1AA_20150713T170348_20160613T170340_VVP336_INT80_G_weF_F19A",
        "S1AA_20150502T170345_20150619T170347_VVP048_INT80_G_weF_DC59",
        "S1AA_20150713T170348_20160707T170341_VVP360_INT80_G_weF_603E",
        "S1AA_20150526T170346_20150619T170347_VVP024_INT80_G_weF_30B6",
        "S1AA_20150806T170349_20150830T170340_VVP024_INT80_G_weF_7194",
        "S1AA_20150526T170346_20150713T170348_VVP048_INT80_G_weF_ED30",
        "S1AA_20150806T170349_20150923T170341_VVP048_INT80_G_weF_D4FC",
        "S1AA_20150526T170346_20160520T170338_VVP360_INT80_G_weF_1FD0",
        "S1AA_20150830T170340_20150923T170341_VVP024_INT80_G_weF_F707",
        "S1AA_20150526T170346_20160520T170338_VVP360_INT80_G_weF_DAD6",
        "S1AA_20150830T170340_20151017T170341_VVP048_INT80_G_weF_9BD0",
        "S1AA_20150619T170347_20150713T170348_VVP024_INT80_G_weF_21AE",
        "S1AA_20150830T170340_20160731T170343_VVP336_INT80_G_weF_3BC7",
        "S1AA_20150619T170347_20150806T170349_VVP048_INT80_G_weF_39DA",
        "S1AA_20150923T170341_20151017T170341_VVP024_INT80_G_weF_04E9"
    ],

    ('edgecumbe', 79): [
        'S1AA_20170305T023738_20170410T023739_VVP036_INT80_G_weF_CF4F',
        'S1AA_20170305T023738_20170422T023740_VVP048_INT80_G_weF_6DEA',
        'S1AA_20180312T023745_20180324T023745_VVP012_INT80_G_weF_D681',
        'S1AA_20180312T023745_20180405T023745_VVP024_INT80_G_weF_1011',
        'S1AA_20180312T023745_20180417T023746_VVP036_INT80_G_weF_63E2',
        'S1AA_20180312T023745_20180429T023746_VVP048_INT80_G_weF_50AF',
        'S1AA_20180803T023752_20180920T023754_VVP048_INT80_G_weF_65EF',
        'S1AA_20180803T023752_20190729T023758_VVP360_INT80_G_weF_0FBF',
        'S1AA_20190530T023754_20190717T023757_VVP048_INT80_G_weF_6F18',
        'S1AA_20190717T023757_20190810T023759_VVP024_INT80_G_weF_48A0',
        'S1AA_20190717T023757_20190822T023759_VVP036_INT80_G_weF_5F73',
        'S1AA_20190810T023759_20190903T023800_VVP024_INT80_G_weF_1BDC',
        'S1AA_20190822T023759_20190903T023800_VVP012_INT80_G_weF_CCEB',
        'S1AA_20190915T023800_20191102T023801_VVP048_INT80_G_weF_E850',
        'S1AA_20200313T023758_20200430T023759_VVP048_INT80_G_weF_70EC',
        'S1AA_20200325T023758_20200430T023759_VVP036_INT80_G_weF_28B2',
        'S1AA_20200430T023759_20200512T023800_VVP012_INT80_G_weF_BCF7',
        'S1AA_20200816T023805_20210904T023812_VVP384_INT80_G_weF_14B5',
        'S1AA_20201003T023807_20201120T023807_VVP048_INT80_G_weF_B617',
        'S1AA_20201015T023807_20201120T023807_VVP036_INT80_G_weF_CC8D',
        'S1AA_20201027T023807_20201120T023807_VVP024_INT80_G_weF_0C15',
        'S1AA_20210320T023803_20210413T023804_VVP024_INT80_G_weF_32E8',
        'S1AA_20210320T023803_20210425T023805_VVP036_INT80_G_weF_0866',
        'S1AA_20210401T023804_20210425T023805_VVP024_INT80_G_weF_B35A',
        'S1AA_20210413T023804_20210425T023805_VVP012_INT80_G_weF_553D',
        'S1AA_20210413T023804_20210519T023806_VVP036_INT80_G_weF_23FF',
        'S1AA_20210519T023806_20210624T023808_VVP036_INT80_G_weF_F836',
        'S1AA_20210624T023808_20210730T023810_VVP036_INT80_G_weF_59E5',
        'S1AA_20211022T023813_20211127T023812_VVP036_INT80_G_weF_BE2A',
        'S1AA_20220315T023809_20220420T023810_VVP036_INT80_G_weF_5B50',
        'S1AA_20220619T023814_20220806T023817_VVP048_INT80_G_weF_B1EA',
        'S1AA_20220701T023815_20230322T023815_VVR264_INT80_G_weF_F4EA',
        'S1AA_20221204T023818_20221228T023817_VVR024_INT80_G_weF_726D',
        'S1AA_20221204T023818_20230202T023815_VVR060_INT80_G_weF_1868',
        'S1AA_20230226T023815_20230310T023815_VVP012_INT80_G_weF_DA04'
    ],

    ('ukinrek', 102): [
        "S1AA_20150317T164607_20150410T164608_VVP024_INT80_G_weF_BE7F",
        "S1AA_20150528T164611_20150621T164612_VVP024_INT80_G_weF_D572",
        "S1AA_20150317T164607_20150504T164609_VVP048_INT80_G_weF_9A03",
        "S1AA_20150528T164611_20150715T164613_VVP048_INT80_G_weF_5F9C",
        "S1AA_20150410T164608_20150504T164609_VVP024_INT80_G_weF_F52D",
        "S1AA_20150621T164612_20150715T164613_VVP024_INT80_G_weF_8B14",
        "S1AA_20150410T164608_20150528T164611_VVP048_INT80_G_weF_AC22",
        "S1AA_20150621T164612_20150808T164614_VVP048_INT80_G_weF_4B98",
        "S1AA_20150410T164608_20160428T164609_VVP384_INT80_G_weF_700E",
        "S1AA_20150715T164613_20150808T164614_VVP024_INT80_G_weF_A7F9",
        "S1AA_20150504T164609_20150528T164611_VVP024_INT80_G_weF_D50A",
        "S1AA_20150715T164613_20160709T164614_VVP360_INT80_G_weF_30F5",
        "S1AA_20150504T164609_20150621T164612_VVP048_INT80_G_weF_0AE1",
        "S1AA_20150808T164614_20150925T164616_VVP048_INT80_G_weF_7208",
        "S1AA_20160709T164614_20160802T164615_VVP024_INT80_G_weF_54E3",
        "S1AA_20160709T164614_20160826T164616_VVP048_INT80_G_weF_D57D",
        "S1AA_20160311T164608_20160404T164609_VVP024_INT80_G_weF_8CBD",
        "S1AA_20160802T164615_20160826T164616_VVP024_INT80_G_weF_2076",
        "S1AA_20160311T164608_20160428T164609_VVP048_INT80_G_weF_20DB",
        "S1AA_20160802T164615_20160919T164617_VVP048_INT80_G_weF_7FF3",
        "S1AA_20160404T164609_20160428T164609_VVP024_INT80_G_weF_C0BB",
        "S1AA_20160826T164616_20160919T164617_VVP024_INT80_G_weF_AAF7",
        "S1AA_20160428T164609_20160615T164612_VVP048_INT80_G_weF_8212",
        "S1AB_20160311T164608_20170324T164541_VVP378_INT80_G_weF_3868",
        "S1AA_20160615T164612_20160709T164614_VVP024_INT80_G_weF_499D",
        "S1AB_20160428T164609_20170417T164542_VVP354_INT80_G_weF_0724",
        "S1AA_20160615T164612_20160802T164615_VVP048_INT80_G_weF_7F6D",
        "S1AB_20160919T164617_20161019T164539_VVP030_INT80_G_weF_CC7F"
    ],

    ('cleveland', 117): [
        "S1BB_20161020T172817_20161113T172817_VVP024_INT80_G_weF_4D7D"
    ],

    ('vsevidof', 117): [
        "S1BB_20161020T172817_20161113T172817_VVP024_INT80_G_weF_4D7D"
    ],
}
