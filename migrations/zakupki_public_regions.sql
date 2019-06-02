create table regions
(
  code               varchar not null,
  name               varchar not null,
  "Federal district" varchar not null,
  "Economic region"  varchar not null
);

alter table regions
  owner to macbook;

create unique index regions_code_uindex
  on regions (code);

INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('Empty', 'Empty', 'Empty', 'Empty');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('1', 'Adygea', 'Southern', 'North Caucasus');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('2', 'Bashkortostan', 'Volga', 'Ural');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('3', 'Buryatia', 'Siberian', 'East Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('4', 'Altai Republic', 'Siberian', 'West Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('5', 'Dagestan', 'North Caucasian', 'North Caucasus');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('6', 'Ingushetia', 'North Caucasian', 'North Caucasus');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('7', 'Kabardino-Balkaria', 'North Caucasian', 'North Caucasus');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('8', 'Kalmykia', 'Southern', 'Volga');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('9', 'Karachay-Cherkessia', 'North Caucasian', 'North Caucasus');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('10', 'Republic of Karelia', 'Northwestern', 'Northern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('11', 'Komi Republic', 'Northwestern', 'Northern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('12', 'Mari El', 'Volga', 'Volga-Vyatka');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('13', 'Mordovia', 'Volga', 'Volga-Vyatka');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('14', 'Sakha Republic', 'Far Eastern', 'Far Eastern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('15', 'North Ossetia-Alania', 'North Caucasian', 'North Caucasus');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('16', 'Tatarstan', 'Volga', 'Volga');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('17', 'Tuva', 'Siberian', 'East Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('18', 'Udmurtia', 'Volga', 'Ural');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('19', 'Khakassia', 'Siberian', 'East Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('20', 'Chechnya', 'North Caucasian', 'North Caucasus');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('21', 'Chuvashia', 'Volga', 'Volga-Vyatka');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('22', 'Altai Krai', 'Siberian', 'West Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('75', 'Zabaykalsky Krai', 'Siberian', 'East Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('41', 'Kamchatka Krai', 'Far Eastern', 'Far Eastern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('23', 'Krasnodar Krai', 'Southern', 'North Caucasus');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('24', 'Krasnoyarsk Krai', 'Siberian', 'East Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('59', 'Perm Krai', 'Volga', 'Ural');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('25', 'Primorsky Krai', 'Far Eastern', 'Far Eastern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('26', 'Stavropol Krai', 'North Caucasian', 'North Caucasus');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('27', 'Khabarovsk Krai', 'Far Eastern', 'Far Eastern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('28', 'Amur Oblast', 'Far Eastern', 'Far Eastern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('29', 'Arkhangelsk Oblast', 'Northwestern', 'Northern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('30', 'Astrakhan Oblast', 'Southern', 'Volga');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('31', 'Belgorod Oblast', 'Central', 'Central Black Earth');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('32', 'Bryansk Oblast', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('33', 'Vladimir Oblast', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('34', 'Volgograd Oblast', 'Southern', 'Volga');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('35', 'Vologda Oblast', 'Northwestern', 'Northern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('36', 'Voronezh Oblast', 'Central', 'Central Black Earth');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('37', 'Ivanovo Oblast', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('38', 'Irkutsk Oblast', 'Siberian', 'East Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('39', 'Kaliningrad Oblast', 'Northwestern', 'Kaliningrad');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('40', 'Kaluga Oblast', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('42', 'Kemerovo Oblast', 'Siberian', 'West Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('43', 'Kirov Oblast', 'Volga', 'Volga-Vyatka');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('44', 'Kostroma Oblast', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('45', 'Kurgan Oblast', 'Ural', 'Ural');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('46', 'Kursk Oblast', 'Central', 'Central Black Earth');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('47', 'Leningrad Oblast', 'Northwestern', 'Northwestern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('48', 'Lipetsk Oblast', 'Central', 'Central Black Earth');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('49', 'Magadan Oblast', 'Far Eastern', 'Far Eastern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('50', 'Moscow Oblast', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('51', 'Murmansk Oblast', 'Northwestern', 'Northern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('52', 'Nizhny Novgorod Oblast', 'Volga', 'Volga-Vyatka');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('53', 'Novgorod Oblast', 'Northwestern', 'Northwestern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('54', 'Novosibirsk Oblast', 'Siberian', 'West Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('55', 'Omsk Oblast', 'Siberian', 'West Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('56', 'Orenburg Oblast', 'Volga', 'Ural');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('57', 'Oryol Oblast', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('58', 'Penza Oblast', 'Volga', 'Volga');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('60', 'Pskov Oblast', 'Northwestern', 'Northwestern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('61', 'Rostov Oblast', 'Southern', 'North Caucasus');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('62', 'Ryazan Oblast', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('63', 'Samara Oblast', 'Volga', 'Volga');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('64', 'Saratov Oblast', 'Volga', 'Volga');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('65', 'Sakhalin Oblast', 'Far Eastern', 'Far Eastern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('66', 'Sverdlovsk Oblast', 'Ural', 'Ural');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('67', 'Smolensk Oblast', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('68', 'Tambov Oblast', 'Central', 'Central Black Earth');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('69', 'Tver Oblast', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('70', 'Tomsk Oblast', 'Siberian', 'West Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('71', 'Tula Oblast', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('72', 'Tyumen Oblast', 'Ural', 'West Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('73', 'Ulyanovsk Oblast', 'Volga', 'Volga');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('74', 'Chelyabinsk Oblast', 'Ural', 'Ural');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('76', 'Yaroslavl Oblast', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('79', 'Jewish Autonomous Oblast', 'Far Eastern', 'Far Eastern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('83', 'Nenets Autonomous Okrug', 'Northwestern', 'Northern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('86', 'Khanty-Mansi Autonomous Okrug', 'Ural', 'West Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('87', 'Chukotka Autonomous Okrug', 'Far Eastern', 'Far Eastern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('89', 'Yamalo-Nenets Autonomous Okrug', 'Ural', 'West Siberian');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('77', 'Moscow', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('78', 'Saint Petersburg', 'Northwestern', 'Northwestern');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('97', 'Moscow', 'Central', 'Central');
INSERT INTO public.regions (code, name, "Federal district", "Economic region") VALUES ('00', 'Empty', 'Empty', 'Empty');