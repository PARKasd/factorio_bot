
import nextcord
import json
import requests
import os
import zipfile
import subprocess
client = nextcord.Client()
token = ""
tokenfact = ""

def dw_embed(title,name,link):
    Embed_1 = nextcord.Embed(title=title, color=0x00ff00)
    Embed_1.add_field(name=name, value=link)
    return Embed_1
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    desti = os.getcwd()
    cmd = f'./factorio/bin/x64/factorio --start-server {desti}/factorio/bin/x64/saves/my-save.zip --server-settings {desti}/factorio/bin/x64/server-settings.json'
    global run
    run = subprocess.Popen(cmd.split(" "))
allowed_ids = {
    "0WON": 462149045268512768,

}
admin= {
    "0WON": 462149045268512768,
    "Dudals": 390048359089569793,
}
allowed_set = set()
admin_set =set()
for id in admin.values():
        admin_set.add(id)
for id in allowed_ids.values():
        allowed_set.add(id)
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!add"):
        if message.author.id in list(admin_set):
            add_id = message.content.replace("!add","").replace("<@!","").replace(">","").replace(" ","")
            print(add_id)
            await message.channel.send(f"adding <@!{add_id}>")
            allowed_set.add(add_id)
        else:
            await message.channel.send("권한이 없으시네영")
    if message.content.startswith('!start'):
        desti = os.getcwd()
        cmd = f'./factorio/bin/x64/factorio --start-server {desti}/factorio/bin/x64/saves/my-save.zip --server-settings {desti}/factorio/bin/x64/server-settings.json'
        global run
        run = subprocess.Popen(cmd.split(" "))
    if message.content.startswith("!kill"):
        run.kill()


    if message.content.startswith("!mod"):
        print(message.author.id)
        def is_correct(m):
            return m.author == message.author and m.content
        embed = nextcord.Embed(title="모드제어판", description="factorio.0won.org 모드 제어판입니다", color=0x8080ff)
        embed.add_field(name="1. 모드설정", value="모드를 추가/제거합니다", inline=False)
        embed.add_field(name="2. 모드상황", value="활성화된 모드를 보여줍니다", inline=False)
        embed.add_field(name="3. 종료", value="모드 수정을 취소합니다", inline=False)
        embed.add_field(name="4. 권한요청", value="모드 수정 권한을 요청합니다", inline=False)
        await message.channel.send(embed=embed)
        agreement1 = await client.wait_for('message', check=is_correct, timeout=30.0)
        if agreement1.content == "1":
                if message.author.id in list(allowed_set):
                    embed1 = nextcord.Embed(title="모드설정", description="factorio.0won.org 모드 설정입니다", color=0xff99cc)
                    embed1.add_field(name="1. 모드추가", value="모드를 추가합니다", inline=False)
                    embed1.add_field(name="2. 모드제거", value="모드를 제거합니다", inline=False)
                    embed1.add_field(name="3. 모드 업데이트", value="모드 업데이트를 확인하고 업데이트 합니다", inline=False)
                    await message.channel.send(embed=embed1)
                    agreement = await client.wait_for('message', check=is_correct, timeout=30.0)
                    if agreement.content == "1":
                        await message.channel.send(
                            "만약 모드를 적용하고 싶으시다면, https://mods.factorio.com/ 에서 모드를 찾아서 링크를 첨부해주세요!")
                        await message.channel.send(f"등록할 링크를 제공해주세요!")
                        agreement = await client.wait_for('message', check=is_correct, timeout=30.0)
                        if agreement.content.find("factorio") != -1:
                            mod_name = agreement.content.split("mod/")[1]
                            url = f'https://mods.factorio.com/api/mods/{mod_name}'
                            await message.channel.send(embed=dw_embed("모드 설치", mod_name, url))
                            response = requests.get(url)
                            response_json = json.loads(response.text)
                            resulta = response_json['releases'][len(response_json["releases"]) - 1]["download_url"]
                            print(resulta)
                            url_download = f"https://mods.factorio.com{resulta}?username=0won2&token={tokenfact}"
                            r = requests.get(url_download)
                            with open(response_json['releases'][len(response_json["releases"]) - 1]["file_name"],'wb') as outfile:
                                outfile.write(r.content)
                            await message.channel.send("성공적으로 다운로드 되었습니다")
                            await message.channel.send("추가 필수 설치 모드가 있는지 찾아보겠습니다.")

                            mod_zip = zipfile.ZipFile(f"{response_json['releases'][len(response_json['releases']) - 1]['file_name']}")
                            try:
                                mod_zip.extract(f"{response_json['name']}/info.json",os.getcwd())
                                with open(f"{os.getcwd()}/{response_json['name']}/info.json") as f:
                                    essential_json = json.load(f)
                            except KeyError:
                                mod_zip.extract(f"{response_json['name']}_{response_json['releases'][len(response_json['releases']) - 1]['version']}/info.json", os.getcwd())
                                with open(f"{os.getcwd()}/{response_json['name']}_{response_json['releases'][len(response_json['releases']) - 1]['version']}/info.json") as f:
                                    essential_json = json.load(f)
                            mod_zip.close()
                            try:
                                src = f"{os.getcwd()}/{response_json['releases'][len(response_json['releases']) - 1]['file_name']}"
                                des = f"{os.getcwd()}/factorio/mods/{response_json['releases'][len(response_json['releases']) - 1]['file_name']}"
                                os.rename(src, des)
                            except FileExistsError:
                                await message.channel.send("이미 있는 모드입니다. 업데이트를 하실목적이라면 업데이트 창을 이용해주세요")
                            print(essential_json)
                            essential_list = list()
                            count = 0
                            embed_mod = nextcord.Embed(title="추가 모드들", color=0xff99cc)
                            while count != 1000:
                                    essential_list.append(essential_json["dependencies"][count].replace("~ ","").split(" ")[0])
                                    if essential_json["dependencies"][count].replace("~ ","").split(" ")[0] != "?" and essential_json["dependencies"][count].replace("~ ","").split(" ")[0] != "base":
                                        embed_mod.add_field(name="⠀", value=f"{count+1}.{essential_list[count]}", inline=False)
                                    if essential_json["dependencies"][count].startswith("?"):
                                        del essential_list[count]
                                        del essential_list[0]
                                        count = 999
                                    count +=1

                            if len(essential_list) == 0:
                                await message.channel.send("추가 모드가 필요하지 않습니다")
                            else:
                                msg = await message.channel.send(embed=embed_mod)
                                await message.channel.send("추가 모드를 설치합니다. 시간이 소요될수 있습니다")

                                embed5 = nextcord.Embed(title="추가모드 설치", color=0xafeeee)
                                msg = await message.channel.send(embed=embed5)
                                for s in range(len(essential_list)):
                                    print(s)
                                    mod_name = essential_list[s]
                                    url = f'https://mods.factorio.com/api/mods/{mod_name}'
                                    embed5.add_field(name=mod_name, value=url, inline=False)
                                    await msg.edit(embed=embed5)
                                    response = requests.get(url)
                                    response_json = json.loads(response.text)
                                    resulta = response_json['releases'][len(response_json["releases"]) - 1]["download_url"]
                                    url_download = f"https://mods.factorio.com{resulta}?username=0won2&token={tokenfact}"
                                    r = requests.get(url_download)
                                    with open(response_json['releases'][len(response_json["releases"]) - 1]["file_name"], 'wb') as outfile:
                                        outfile.write(r.content)
                                    try:
                                        src = f"{os.getcwd()}/{response_json['releases'][len(response_json['releases']) - 1]['file_name']}"
                                        des = f"{os.getcwd()}/factorio/mods/{response_json['releases'][len(response_json['releases']) - 1]['file_name']}"
                                        os.rename(src, des)
                                    except FileExistsError:
                                        await message.channel.send("이미 있는 모드입니다.")
                            run.kill()
                            desti = os.getcwd()
                            cmd = f'./factorio/bin/x64/factorio --start-server {desti}/factorio/bin/x64/saves/my-save.zip --server-settings {desti}/factorio/bin/x64/server-settings.json'
                            run = subprocess.Popen(cmd.split(" "))
                            await message.channel.send("재시작하였습니다.")

                        else:
                            await message.channel.send("등록을 취소합니다!")
                    if agreement.content == "2":
                        embed_del = nextcord.Embed(title="모드 명단", description="설치되어 있는 모드를 보여줍니다", color=0x123456)
                        msg = await message.channel.send(embed=embed_del)
                        mod_list = os.listdir(f"{os.getcwd()}/factorio/mods")
                        print(mod_list)
                        update_list = []
                        for a in range(len(mod_list)):
                            if mod_list[a].endswith("zip"):
                                mod_version = mod_list[a].replace('.zip', '')
                                mod_version = mod_version.split("_")
                                version = mod_version[len(mod_version) - 1]
                                del mod_version[len(mod_version) - 1]
                                mod = '_'.join(mod_version)
                                print(mod)
                                embed_del.add_field(name=a+1, value=mod, inline=False)
                        await msg.edit(embed=embed_del)
                        embed_ex = nextcord.Embed(title="삭제법", description="삭제 방법을 알려드립니다.", color=0xff0000)
                        embed_ex.add_field(name="방법 1", value="삭제하고 싶은 모드의 번호를 입력 ex) 15", inline=False)
                        embed_ex.add_field(name="방법 2", value="삭제하고 싶은 모드들의 번호를 입력 ex) 1,4,5", inline=False)
                        await message.channel.send(embed = embed_ex)
                        agreementa = await client.wait_for('message', check=is_correct, timeout=60.0)
                        rem_list = agreementa.content.split(",")
                        rem_list_embed = nextcord.Embed(title="삭제 대상 모드", description="같이 설치된 필수모드도 삭제됩니다.", color=0xff0000)
                        msg = await message.channel.send(embed=rem_list_embed)
                        run.kill()
                        for a in range(len(rem_list)):
                            rem_mod_list = []
                            b = int(rem_list[a])
                            rem_mod_list.append(mod_list[b-1])
                            mod_version = mod_list[b-1].replace('.zip', '')
                            mod_version = mod_version.split("_")
                            version = mod_version[len(mod_version) - 1]
                            del mod_version[len(mod_version) - 1]
                            name = '_'.join(mod_version)
                            rem_list_embed.add_field(name=int(a)+1, value=name, inline=False)
                            a_all = a
                        await msg.edit(embed=rem_list_embed)
                        for a in range(len(rem_mod_list)):
                            mod_zip = zipfile.ZipFile(f"factorio/mods/{rem_mod_list[a]}")
                            mod_version = rem_mod_list[a].replace('.zip', '')
                            mod_version = mod_version.split("_")
                            version = mod_version[len(mod_version) - 1]
                            del mod_version[len(mod_version) - 1]
                            name = '_'.join(mod_version)
                            try:
                                mod_zip.extract(f"{name}/info.json", os.getcwd())
                                with open(f"{os.getcwd()}/{name}/info.json") as f:
                                    essential_json = json.load(f)
                            except KeyError:
                                mod_zip.extract(
                                    f"{rem_mod_list[a].replace('.zip', '')}/info.json",
                                    os.getcwd())
                                with open(
                                        f"{os.getcwd()}/{rem_mod_list[a].replace('.zip', '')}/info.json") as f:
                                    essential_json = json.load(f)
                            mod_zip.close()
                            essential_list = list()
                            count = 0
                            while count != 1000:
                                essential_list.append(
                                    essential_json["dependencies"][count].replace("~ ", "").split(" ")[0])
                                if essential_json["dependencies"][count].replace("~ ", "").split(" ")[0] != "?" and \
                                        essential_json["dependencies"][count].replace("~ ", "").split(" ")[0] != "base":
                                    rem_list_embed.add_field(name=int(a_all)+2, value=essential_json["dependencies"][count].replace("~ ", "").split(" ")[0], inline=False)
                                    a_all += 1
                                if essential_json["dependencies"][count].startswith("?"):
                                    del essential_list[count]
                                    del essential_list[0]
                                    count = 999
                                count += 1
                            await msg.edit(embed=rem_list_embed)
                            final = rem_mod_list + essential_list
                            for a in range(len(final)):
                                for f_name in os.listdir(f"{os.getcwd()}/factorio/mods"):
                                    if f_name.startswith(final[a]):
                                        os.remove(f"{os.getcwd()}/factorio/mods/{f_name}")
                            await msg.edit("완료되었습니다!")
                            run.kill()
                            desti = os.getcwd()
                            cmd = f'./factorio/bin/x64/factorio --start-server {desti}/factorio/bin/x64/saves/my-save.zip --server-settings {desti}/factorio/bin/x64/server-settings.json'

                            run = subprocess.Popen(cmd.split(" "))







                    if agreement.content == "3":
                        embed_update = nextcord.Embed(title="모드 업데이트 필요", description="업데이트가 필요한 모드들을 보여줍니다", color=0xb698f9)
                        msg = await message.channel.send(embed=embed_update)
                        mod_list = os.listdir(f"{os.getcwd()}/factorio/mods")
                        print(mod_list)
                        update_list =[]
                        for a in range(len(mod_list)):
                            if mod_list[a].endswith("zip"):
                                mod_version = mod_list[a].replace('.zip', '')
                                mod_version = mod_version.split("_")
                                version = mod_version[len(mod_version) - 1]
                                del mod_version[len(mod_version) - 1]
                                mod = '_'.join(mod_version)
                                print(mod_list[a])
                                url = f'https://mods.factorio.com/api/mods/{mod}'
                                response = requests.get(url)
                                response_json = json.loads(response.text)
                                version2 = response_json['releases'][len(response_json["releases"]) - 1]["version"]
                                if version != version2:
                                    embed_update.add_field(name=mod, value=f"현재 설치된 버전은 {version}이며 최신버전은 {version2} 입니다.", inline=False)
                                    update_list.append(f"{mod}//{version}")

                        await msg.edit(embed=embed_update)
                        run.kill()
                        embed_updating = nextcord.Embed(title="업데이트 모드", description="현재 업데이트 중인 모드입니다.", color=0xff99cc)
                        msg = await message.channel.send(embed=embed_updating)
                        for a in range(len(update_list)):
                            url = f"https://mods.factorio.com/api/mods/{update_list[a].split('//')[0]}"
                            embed_updating.add_field(name=update_list[a].split('//')[0],value=url , inline=False)
                            await msg.edit(embed=embed_updating)
                            response = requests.get(url)
                            response_json = json.loads(response.text)
                            resulta = response_json['releases'][len(response_json["releases"]) - 1]["download_url"]
                            url_download = f"https://mods.factorio.com{resulta}?username=0won2&token={tokenfact}"
                            r = requests.get(url_download)
                            with open(response_json['releases'][len(response_json["releases"]) - 1]["file_name"],'wb') as outfile:
                                outfile.write(r.content)
                            try:
                                os.remove(f'{os.getcwd()}/factorio/mods/{update_list[a].replace("//","_")}.zip')
                                src = f"{os.getcwd()}/{response_json['releases'][len(response_json['releases']) - 1]['file_name']}"
                                des = f"{os.getcwd()}/factorio/mods/{response_json['releases'][len(response_json['releases']) - 1]['file_name']}"
                                os.rename(src, des)
                            except FileExistsError:
                                src = f"{os.getcwd()}/{response_json['releases'][len(response_json['releases']) - 1]['file_name']}"
                                des = f"{os.getcwd()}/factorio/mods/{response_json['releases'][len(response_json['releases']) - 1]['file_name']}"
                                os.rename(src, des)
                        await message.channel.send("완료되었습니다.")
                        run





                else:
                    embed2 = nextcord.Embed(title="거절", description="권한이 없으셔서 모드 접근이 막혀있습니다", color=0xff0000)
                    embed2.add_field(name="1. 권한요청", value="모드 수정 권한을 요청합니다", inline=False)
                    embed2.add_field(name="2. 종료", value="모드 제어판을 종료합니다", inline=False)
                    await message.channel.send(embed=embed2)
                    agreement2 = await client.wait_for('message', check=is_correct, timeout=30.0)
                    if agreement2.content == "1":
                        await message.channel.send(f"관리자들에게 전달되었습니다. 심사후 권한 부여 여부를 알려드립니다.")
                    if agreement2.content == "2":
                        await message.channel.send("도움을 드리지 못해 죄송합니다.")
        elif agreement1.content == "2":
                mod_list = os.listdir(f"{os.getcwd()}/factorio/mods")
                print(mod_list)
                embed6 = nextcord.Embed(title="모드들입니다!", description="공원서버에 다운로드 되어 있는 모드들을 보여줍니다", color=0xf6546a)
                for a in range(len(mod_list)):
                    if mod_list[a].endswith("zip"):
                        mod_version = mod_list[a].replace('.zip','')
                        mod_version = mod_version.split("_")
                        version = mod_version[len(mod_version) -1]
                        del mod_version[len(mod_version) -1]
                        mod = '_'.join(mod_version)
                        embed6.add_field(name=f"{mod}", value=f"설치된 버전:{version}", inline=False)
                        print(mod_list[a])
                await message.channel.send(embed=embed6)


        elif agreement1.content == "3":
                await message.channel.send("취소되었습니다!")
        elif agreement1.content == "4":
                await message.channel.send("관리자들에게 전달되었습니다. 심사후 권한 부여 여부를 알려드립니다.")
client.run('token')
