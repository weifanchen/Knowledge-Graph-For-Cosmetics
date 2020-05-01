<template>
    <div style="width:100%;display:flex;background-color:#F6F7FB;">
        <div id='left' style="width:7%;background-color:#3A4161;">
            <div style="height:95px;padding: 10px 15px;color: #fff;font-family:'Anton';font-size:24px;background-color:#230F35;">Cos<br>Chem</div>
            <!-- <div style="height:50px;margin:15px;padding: 10px 0px;color: #230F35;font-family:'Anton';font-size:12px;writing-mode: vertical-lr;text-orientation: mixed;">INF558 Building Knowledge Graph</div> -->
        </div>
        <div id='right' style="width:93%; display:block;background-color:#F6F7FB;">
            <div id="tabs" class="container">
            
                <div class="tabs">
                    <a v-on:click="activetab=1; productLoaded=fasle" v-bind:class="[ activetab === 1 ? 'active' : '' ]">Product</a>
                    <a v-on:click="activetab=2" v-bind:class="[ activetab === 2 ? 'active' : '' ]">Ingredient</a>
                    <a v-on:click="activetab=3;clickAdvanced=false" v-bind:class="[ activetab === 3 ? 'active' : '' ]">Advanced</a>
                </div>
                <div class="content">
                    <div v-if="activetab === 1" class="tabcontent">
                        <div class='basic-search'>
                            <AutoComplete
                                v-model="value"
                                @on-search="filterMethod"
                                @on-select="selectMethod"
                                placeholder="let's get your product"
                                style="width:50%; max-height: 100px;">
                                <Option v-for="item in matches" :value="item.name" :key="item.id">{{item.name}}</Option>
                            </AutoComplete>
                            <div class='input-field'>
                                <!-- <input id='search' type='text' placeholder='What are you looking for?'> -->
                                <div class="icon-wrap">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" @click="getProduct(selected)">
                                        <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"></path>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div v-if="activetab === 2" class="tabcontent">
                        <div class='basic-search'>
                            <Select v-model="ings" filterable placeholder="pick the ingredient" style='width:50%' @on-select="selectIng">
                                <Option v-for="item in ingredient" :value="item.name" :key="item.ingredient_id">{{item.name}}</Option>
                            </Select>
                            <div class='input-field'>
                                <div class="icon-wrap">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" @click="getIng(selecteding)">
                                        <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"></path>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div v-if="activetab === 3" class="tabcontent">
                        <div style='display:flex; padding: 0px 20px;'>
                            <div style='width:223.97px;margin-right: 40px;'>
                                <p style='margin-bottom: 5px;'>Categories</p>
                                <Select v-model="selectCat" multiple placeholder='Choose Category' style="width: 223.97px;">
                                    <OptionGroup label="Moisturizers">
                                        <Option v-for="item in categoryList.Moisturizers" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="Treatments">
                                        <Option v-for="item in categoryList.Treatments" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>      
                                    <OptionGroup label="Cleansers">
                                        <Option v-for="item in categoryList.Cleansers" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="Masks">
                                        <Option v-for="item in categoryList.Masks" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup> 
                                    <OptionGroup label="Eye Care">
                                        <Option v-for="item in categoryList.EyeCare" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="Sun Care">
                                        <Option v-for="item in categoryList.SunCare" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup> 
                                    <OptionGroup label="Lip Treatments">
                                        <Option v-for="item in categoryList.LipTreatments" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="Self Tanners">
                                        <Option v-for="item in categoryList.SelfTanners" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>  
                                    <OptionGroup label="Skincare">
                                        <Option v-for="item in categoryList.Skincare" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="Wellness">
                                        <Option v-for="item in categoryList.Wellness" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>      
                                    <OptionGroup label="Body Moisturizers">
                                        <Option v-for="item in categoryList.BodyMoisturizers" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="High Tech Tools">
                                        <Option v-for="item in categoryList.HighTechTools" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup> 
                                    <OptionGroup label="Hair Styling Treatments">
                                        <Option v-for="item in categoryList.HairStylingTreatments" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>
                                    <OptionGroup label="Bath Shower">
                                        <Option v-for="item in categoryList.BathShower" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup> 
                                    <OptionGroup label="Others">
                                        <Option v-for="item in categoryList.Others" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                    </OptionGroup>    
                                </Select>
                            </div>
                            <div class='filter' style='width:223.97px;margin-right: 30px;'>
                                <p style='width:223.97px;margin-bottom: 5px;'>Brand</p>
                                <Select v-model="bra" placeholder='Choose a brand'>
                                    <Option v-for="item in brand" :value="item" :key="item">{{ item }}</Option>
                                </Select>
                            </div>

                            <div class='filter' style='width: 223.97px;padding-left:15px'>
                                <p>Acne</p>
                                <label><input v-model="acne" type="radio" name="acne" v-bind:value="1"/><span data-points="1">1</span></label>
                                <label><input v-model="acne" type="radio" name="acne" v-bind:value="2"/><span data-points="2">2</span></label>
                                <label><input v-model="acne" type="radio" name="acne" v-bind:value="3"/><span data-points="3">3</span></label>
                                <label><input v-model="acne" type="radio" name="acne" v-bind:value="4"/><span data-points="4">4</span></label>
                                <label><input v-model="acne" type="radio" name="acne" v-bind:value="5"/><span data-points="5">5</span></label>
                            </div>
                            <div class='filter' style='width:17%;padding-left:15px;padding-right:15px;'>
                                <p>Price</p>
                                <Slider v-model="pricegap" range :min="0" :max="500" :step="10" style="margin-left:4px;"/>
                            </div>
                            <div style='width:223.97px;margin-left:13px;'>
                            </div>
                        </div>
                        <div style='display:flex; padding: 0px 20px;margin-top:15px;'>
                            <div style='width:223.97px;margin-right: 40px;'>
                                <p style='margin-bottom: 5px;'>Functions</p>
                                <Select style='width:223.97px;' v-model="func" multiple placeholder='Choose desired functions'>
                                    <Option v-for="item in funcList" :value="item" :key="item">{{ item }}</Option>
                                </Select>
                            </div>
                            <div style='width:223.97px;margin-right: 30px;'>
                                <p style='margin-bottom: 5px;'>Avoid</p>
                                <Select style='width:223.97px' v-model="fda" multiple placeholder='Choose some restrictions'>
                                    <Option v-for="item in avoidList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </Select>
                            </div>
                            <div class='filter' style='width:223.97px;padding-left:15px;'>
                                <p>Irritant</p>
                                <label><input v-model="irri" type="radio" name="irri" v-bind:value="1"/><span data-points="1">1</span></label>
                                <label><input v-model="irri" type="radio" name="irri" v-bind:value="2"/><span data-points="2">2</span></label>
                                <label><input v-model="irri" type="radio" name="irri" v-bind:value="3"/><span data-points="3">3</span></label>
                                <label><input v-model="irri" type="radio" name="irri" v-bind:value="4"/><span data-points="4">4</span></label>
                                <label><input v-model="irri" type="radio" name="irri" v-bind:value="5"/><span data-points="5">5</span></label>
                            </div>
                            <div style='width:17%;padding-left:10px;'>
                                <p>Match Collection</p>
                                <div>
                                    <label class="switch">
                                        <input v-model="coll" type="checkbox">
                                        <span class="slider"></span>
                                    </label>
                                </div>
                                <!-- <iSwitch>Fit my collections!</iSwitch> -->
                                <!-- <label><input v-model="coll" type="checkbox" name="collection" /><span></span>   Fit my collections!</label>                                 -->
                                <!-- <Checkbox v-model="coll"></Checkbox>
                                <span><strong>    Fit my collections!   </strong></span> -->
                            </div>
                            <div class='filter' style='width:223.97px;padding-top:20px;padding-left:20px'>
                                <Button shape="circle" icon="ios-search" @click="getMsg">Filter</Button>
                                <!-- <Button shape="circle" icon="ios-search" @click="getMsg"></Button> -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class='result' style="margin: 0px 35px; padding:10px;">
                <div v-if="activetab === 1 && productLoaded" class="tabcontent">
                    <div style="padding: 30px 0 0 30px; display:flex;">
                        <div class='leftPanel' style="width:48%">
                            <div style='display:flex;padding-bottom:20px;'>
                                <img v-bind:src=productDict[selected.id].image style="max-height:160px;width:140px;border-radius: 20px; border:1.5px solid #F6F4F9">
                                <div style="padding-left: 50px; width:80%;padding-right: 70px;">
                                    <p>{{msg.brand}}</p>
                                    <!-- {{msg}} -->
                                    <p style="font-size:22px; font-weight:bold;color:#505050">{{msg.product_name}}</p> 
                                    <button id="collection" class='add' type="button" @click='putBag'>Add to Collection</button>
                                    <p style="margin-top:20px;"></p>
                                    <div style="width:100%; height:45px">
                                        <p style="float: left"><strong>Category</strong><br>{{msg.minicategory}}</p>
                                        <p style="margin-left: 130px"><strong>Sephora Link</strong><br><a v-bind:href="msg.url" target="_blank">Visit Sephora!</a></p>
                                    </div>
                                    <div style="width:100%; height:45px; margin-top:10px">
                                        <p style="float: left"><strong>Price</strong><br>starts from ${{msg.price}}</p>
                                        <p style="margin-left: 130px"><strong>Size</strong><br>starts from {{msg.size}} oz</p>
                                    </div>
                                </div>
                            </div>
                            <div v-if='similar[selected.id].length'>
                                <p style="font-size:20px;color:#505050; margin-bottom:15px;margin-top:10px">Similar products</p> 
                                <div style='margin-left:5px;margin-right:15px;display: flex'> 
                                    <div class='similar' style='height:120px;width:50%;padding:10px 0px;display:flex;margin-left: 5px;' v-for="item in similar[selected.id].slice(0,2)" v-bind:key="item.id">
                                        <div style='margin-right: 8px;'><img v-bind:src="productDict[item.id].image" style="max-height:160px;width:75px"/></div>
                                        <div style='height:120px;'>
                                            <p class="product" @click="getProduct(item)"><strong>{{item.name}}</strong></p>
                                            <p>{{item.star}} stars</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div style="width:51%;margin-top:4%;padding-left:3%;padding-right:2%;border-left:1px solid #C1C1C1">
                                <p style="font-size:20px;color:#505050; margin-bottom:5px;margin-top:10px">Ingredients</p> 
                                <ul style="list-style-type:none;box-shadow: 0 3px 6px rgba(0,0,0,0.01), 0 3px 6px rgba(0,0,0,0.01);">
                                    <li class='ingredient' style='height:50px;padding:15px 15px;border-bottom:0.5px solid #F6F4F9;font-size: 15px;' v-for="item in msg.ingredients" v-bind:key="item.ingredient_id" @click="getIng(item)">
                                        {{item.name}}
                                    </li>
                                </ul>
                        </div>
                    </div>                       
                </div>
                <div v-if="activetab === 2 && ingredientLoaded" class="tabcontent">
                    <div v-if="ingredientLoaded" style="padding: 30px 0 0 30px;min-height:500px;">
                        <p style="font-size:24px; font-weight:bold;color:#505050;margin-bottom:30px;">{{ingmsg.name}}</p> 

                        <div style="padding: 0px 20px;">
                            <div id='ing' style="float: left; width: 30%;">
                                <ul style="list-style-type:none;">
                                    <li v-if = "ingmsg.hasOwnProperty('forumula')"><strong>Chemical Formula</strong></li>
                                    <li v-if = "ingmsg.hasOwnProperty('link')"><strong>PubChem Link</strong></li>
                                    <li v-if = "ingmsg.hasOwnProperty('function')"><strong>Function</strong></li>
                                    <li v-if = "ingmsg.hasOwnProperty('acne')"><strong>Acne</strong></li>
                                    <li v-if = "ingmsg.hasOwnProperty('irritant')"><strong>Irritant</strong></li>
                                    <li v-if = "ingmsg.hasOwnProperty('safety')"><strong>Safety</strong></li>
                                    <li v-if = "ingmsg.hasOwnProperty('synonym')"><strong>Function</strong></li>
                                </ul>
                            
                            </div>
                            <div id='ing' style="float: right; width: 70%;">
                                <ul style="list-style-type:none;">
                                    <li v-if = "ingmsg.hasOwnProperty('forumula')">{{ingmsg.forumula}}</li>
                                    <li v-if = "ingmsg.hasOwnProperty('link')"><a v-bind:href="ingmsg.link" target="_blank">{{ingmsg.link}}</a></li>
                                    <li v-if = "ingmsg.hasOwnProperty('function')"><p v-for="item in ingmsg.function" v-bind:key="item">{{item}}</p></li>
                                    <li v-if = "ingmsg.hasOwnProperty('acne')">{{ingmsg.acne}}</li>
                                    <li v-if = "ingmsg.hasOwnProperty('irritant')">{{ingmsg.irritant}}</li>
                                    <li v-if = "ingmsg.hasOwnProperty('safety')">{{ingmsg.safety}}</li>
                                    <li v-if = "ingmsg.hasOwnProperty('synonym')"><p v-for="item in ingmsg.synonym" v-bind:key="item">{{item}}</p></li>
                                </ul>                           
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="activetab === 3 && msgLoaded" class="tabcontent" style="padding: 50px 100px 50px 50px; ">
                    <div v-if="coll" style="padding-bottom: 15px;margin-bottom: 15px; border-bottom:1px solid #DCDEE2;min-height:100px">
                        <p style="margin-bottom: 15px;"><strong>My collections</strong></p>
                        <!-- <span v-for="item in mycollectfull" v-bind:key="item.id">{{item.name}}, </span> -->
                        <!-- <a v-for="item in mycollectfull" v-bind:key="item.id" @click="awaybag(item)">{{item.name}}</a> -->
                        <Button style="margin-right: 5px;" v-for="item in mycollectfull" v-bind:key="item.id" @click="awaybag(item)" shape="circle" icon="ios-close-circle-outline">{{item.name}}</Button>

                    </div>
                    <!-- {{msg}} -->
                    <div v-if="msgLoaded">
                        <p style="margin-bottom:30px" v-if="msgLoaded">{{listmsg.length}} results</p>
                        <div style="padding: 0px 20px;min-height:700px;">
                            <div id='pro' v-for="item in listmsg" :key="item.id" style="display:flex; height:90px">
                                <div style="float:right;width:90%">
                                    <p id='productname' @click="getProduct(item)"><strong>{{item.product_name}}</strong></p>
                                    <p>{{item.brand}} | {{item.minicategory}}</p>
                                </div>
                                <div style="float:left;width:10%">
                                    <img v-bind:src="productDict[item.product_id].image" style="max-height:160px;width:50px"/>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import categoryList from '@/assets/categoryList.js'

// import product from '@/assets/product3.js'
import product from '@/assets/product.json'
import product_dict from '@/assets/product_dict.json'

import ingredient from '@/assets/ingredients.json'
import axios from 'axios';
import similar from '@/assets/similar_product.json'
import brand from '@/assets/brand.json'


// exmaple query result
// import proexample from '@/assets/proexample.json'
import advexample from '@/assets/advexample.json'

export default{
    mounted(){
        this.suggestions = product;
        this.ingredient = ingredient;
        this.dataLoaded = true;
        this.productDict = product_dict
        // console.log(this.suggestions)
    },
    created(){
        this.categoryList = categoryList;
    },
    data(){
        return{
            // mounted and created
            suggestions:[],
            ingredient:[],
            dataLoaded: false,
            productDict: '',
            categoryList: [],

            // initialize
            activetab: 1,
            brand: brand,
            similar: similar,

            
            // product
            value: '',
            matches: [], 
            selected:'',
            msg: '',
            productLoaded: false,

            
            // ingredient
            ings: '',
            selecteding:'',
            ingmsg: '',
            ingredientLoaded: false,
            
            
            // advanced
            avoidList: [
                    {value: 'Fragrance', label: 'Fragrance'},
                    {value: 'Preservative', label: 'Preservative'},
                    {value: 'Alcohol', label: 'Alcohol'},],
            funcList: ['Anti-allergic', 'Anti-inflammatory', 'Antidandruff', 'Antimicrobial', 'Antioxidant', 'Cellregeneration', 'Deodorant', 'Depilatory', 'Emollient', 'Exfoliator', 'Hair Conditioning', 'Hair Fixative', 'Humectant', 'Moisturizer', 'Nail Conditioning', 'Oral Care', 'Skin Conditioning', 'Smoothing', 'Sunscreen', 'Whitening', 'anti-aging'],
            selectCat: [],
            acne: 1,
            irri: 1,
            safe: 1,
            fda: [],
            func: [],
            bra: '',
            pricegap: [0, 100],
            coll: false,
            
            clickAdvanced: false,
            msgLoaded: false,
            listmsg: '',
            
            // mycollection
            mycollect: [],
            mycollectfull: [],
        }
    },
    methods:{

        // get product
        getProduct(item){
            console.log(item)
            if('product_id' in item){
                this.selected = {'id':item.product_id, 'name':item.product_name}
            }else{
                this.selected = item;
            }
            this.productLoaded = false;
            this.msg ='';
            
            const path = 'http://localhost:5000/';
            axios.get(path,  {
                params: {
                    type: 'Basic',
                    product: this.selected['id'],
                }
                }).then((res) => {
                    console.log(res);
                    this.msg = res.data;
                })
                .catch((error) => {
                    console.error(error);
                });
            this.value = this.selected.name;
            // console.log(this.selected)
            this.productLoaded = true;
            this.activetab = 1;

            if(this.mycollect.includes(this.selected['id'])){
                document.getElementById("collection").innerHTML = "Out of Collection"
                document.getElementById("collection").className = "away"
            }else{
                document.getElementById("collection").innerHTML = "Add to Collection"
                document.getElementById("collection").className = "add"
            }

            // this.msg = proexample;
        },
        
        // get ingredient
        getIng(item){
            console.log(item)
            this.selecteding = item;
            this.ingredientLoaded = false;
            // this.clickIng = true;
            this.ingmsg = false;
            const path = 'http://localhost:5000/';
            axios.get(path,  {
                params: {
                    //product_id: this.selected.product_id 
                    type: 'Compound',
                    // product: this.value,
                    ingredient: this.selecteding['ingredient_id'],
                }
                }).then((res) => {
                    console.log(res);
                    this.ingmsg = res.data;
                })
                .catch((error) => {
                    console.error(error);
                });

            this.ings = item.name;
            this.activetab = 2;
            this.ingredientLoaded = true;
        },

        // get list
        getMsg(){
            this.msgLoaded = false;
            this.listmsg = ''; 
            this.clickAdvanced = true;
            const path = 'http://localhost:5000/';
            
            if(this.coll){
                axios.get(path,  {
                params: {
                    //product_id: this.selected.product_id 
                    type: 'Collection',
                    categories: this.selectCat,
                    brand: this.bra,
                    price: this.pricegap,
                    acne: this.acne,
                    irri: this.irri,
                    fda: this.fda,
                    function: this.func,
                    collection: this.mycollect
                }
                }).then((res) => {
                    console.log(res);
                    this.listmsg = res.data;
                })
                .catch((error) => {
                    console.error(error);
                });
                
                if(this.listmsg!=''){
                    this.msgLoaded = true;
                }
                // this.msg = advexample;

            }else{
                axios.get(path,  {
                params: {
                    //product_id: this.selected.product_id 
                    type: 'Advanced',
                    categories: this.selectCat,
                    brand: this.bra,
                    price: this.pricegap,
                    acne: this.acne,
                    irri: this.irri,
                    fda: this.fda,
                    function: this.func
                }
                }).then((res) => {
                    console.log(res);
                    this.listmsg = res.data;
                })
                .catch((error) => {
                    console.error(error);
                });
                if(this.listmsg!=''){
                    this.msgLoaded = true;
                }
                // this.msg = advexample;
            }
            console.log("Hello")
            this.listmsg = advexample;
            this.msgLoaded = true;
        },

        // autocomplete method
        filterMethod (value) {
            // console.log(value)
            this.matches = this.suggestions.filter(row => { return row.name.toLowerCase().indexOf(value.toLowerCase()) > -1});
        },
        selectMethod (value) {
            this.msg = '';
            this.productLoaded = false;
            // console.log(value)
            this.selected = this.suggestions.filter(row => { return row.name.toLowerCase().indexOf(value.toLowerCase()) > -1})[0];
            console.log(this.selected)
            // this.matches = this.items.filter(row => { return row.name.toLowerCase().indexOf(value.toLowerCase()) > -1});
        },
        
        selectIng (value){
            console.log(value)
            this.selecteding = this.ingredient.filter(row => { return row.name.toLowerCase().indexOf(value.value.toLowerCase()) > -1})[0];
        },

        putBag(item){
            console.log(item)
            if(this.mycollect.includes(this.msg.product_id)){
                this.mycollect = this.mycollect.filter(row => { return row.indexOf(this.msg.product_id) < 0});
                this.mycollectfull = this.mycollectfull.filter(row => { return row.id.indexOf(this.msg.product_id) < 0});
                document.getElementById("collection").innerHTML = "Add to Collection"
                document.getElementById("collection").className = "add"
            }else{
                this.mycollect.push(this.msg.product_id)
                this.mycollectfull.push({id: this.msg.product_id, name: this.msg.product_name})
                document.getElementById("collection").innerHTML = "Out of Collection"
                document.getElementById("collection").className = "away"
            }
            console.log(this.mycollect)
            console.log(this.mycollectfull)
        },
        awaybag(item){
            this.mycollect = this.mycollect.filter(row => { return row.indexOf(item.id) < 0});
            this.mycollectfull = this.mycollectfull.filter(row => { return row.id.indexOf(item.id) < 0});
            console.log(this.mycollect);
            console.log(this.mycollectfull);
            if(this.mycollect.length==0){
                this.coll = false;
            }
            this.getMsg();

        }
        
    }
}
</script>

<style>

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* STYLING */
#result, .container {
    margin: 10px 35px;
    font-family: "Nunito Sans", Arial, Helvetica, sans-serif;
    color: #888;
    padding: 10px;
}

/* Style the tabs */
.tabs {
    overflow: hidden;
    margin-left: 20px;
    padding-bottom: 10px;
    /* margin-bottom: -2px;  */
}

.tabs ul {
    list-style-type: none;
    margin-left: 20px;
}

.tabs a {
    float: left;
    cursor: pointer;
    padding: 6px 20px;
    transition: background-color 0.2s;
    /* border-bottom: 1.5px solid #ccc; */
    border-right: none;
    /* background-color: #f1f1f1; */
    border-radius: 16px;
    font-weight: bold;
    color: #888888;
    margin: 0px 24px 0px 0px;
}

.tabs a:last-child { 
    /* border-right: 1px solid #ccc; */
}

/* Change background color of tabs on hover */
.tabs a:hover {
    /* border-bottom: 1.5px solid #CBCBCB; */
    background-color: #CBCBCB;
    color: #2C3542;
}

/* Styling for active tab */
.tabs a.active {
    /* border-bottom: 1.5px solid #7889B3; */
    background-color: #7889B3;
    color: #fff;
    /* border-bottom: 2px solid #fff; */
    cursor: default;
}

/* Style the tab content */
.tabcontent {
    /* min-height: 730px; */
    padding: 20px 3px;
    /* border-right: 1.2px solid #ccc;
    border-left: 1.2px solid #ccc;
    border-bottom: 1.2px solid #ccc; */
    border-radius: 5px 5px 5px 5px;
    box-shadow: 1.5px 1.5px 6px #e1e1e1;
    margin: 0px 20px;
    background-color: #fff;
}

form {
    width: 100%;
    max-width: 790px;
    margin: 0;
}

/* .searchPanel {
    width: 100%;
} */

.basic-search {
    padding: 0px 0 0 20px;
    margin-bottom: 5px;
    /* box-shadow: 0px 8px 20px 0px rgba(0, 0, 0, 0.15); */
    /* overflow: hidden;
    border-radius: 20px;
    margin-bottom: 5px;
    border: 1.5px solid #FFE659;
    height: 40px;
    width: 40%; */
}

.input-field {
    width: 100%;
    position: relative;
    padding: 0 20px;
}

input {
    height: 100%;
    border: 0;
    display: block;
    width: 100%;
    padding: 10px 80px 10px 40px;
    font-size: 18px;
    height: 36px;
    color: #333333;
    background: transparent;
    border: none;
    outline: none;
    /* background: linear-gradient(to right, #2c6dd5 0%, #2c6dd5 28%, #ff4b5a 91%, #ff4b5a 100%); */
    /* font-family: 'Lato', sans-serif; */
}

::placeholder{
    color: #333333 0.3;
}

.icon-wrap {
    position: absolute;
    top: -15px;
    left: 51%;
    /* right: 0; */
    display: -ms-flexbox;
    display: flex;
    -ms-flex-align: center;
    align-items: center;
    width: 40px;
    height: 100%;
}

path {
    fill: #7889B3;
}

.ivu-select-dropdown {
    min-width: 200px !important;
    width: inherit;
    max-height: 200px;
    overflow: auto;
    margin: 5px 0;
    padding: 10px 10px !important;
    background-color: #fff;
    box-sizing: border-box;
    border-radius: 4px;
    box-shadow: 0 1px 6px rgba(0,0,0,.2);
    position: absolute;
    z-index: 900;
}

.advanced-search{
    padding: 10px 700px 0 20px;
    /* box-shadow: 0px 8px 20px 0px rgba(0, 0, 0, 0.15);
    border-radius: 10px; */
}

.advance-search span {
    font-size: 14px;
    font-weight: bold;
    color: #555;
    display: block;
    margin-bottom: 26px;
}

.filter label {
    /* display: block;  */
    /* padding: 5px;  */
    position: relative; 
    padding-left: 35px;
    /* padding-right: 20px; */
}


.filter label input {display: none;}

.filter label span {
    /* border: 1px solid #ccc; */
    /* background: #f1f1f1; */
    width: 20px;
    height: 20px;
    position: absolute;
    overflow: hidden;
    /* line-height: 1; */
    text-align: center;
    border-radius: 100%;
    font-size: 10pt;
    left: 0;
    top: 50%;
    margin-top: -2px;
}

.filter label span:hover{
   background: #E1E3E7; 
}

/* input:checked + span {
    background: #ccf; 
    border-color: #ccf;} */


.filter input:checked + span[data-points="1"] {
    background: #7f7d33; 
    opacity: 0.6;
    color: #fff;
    }
.filter input:checked + span[data-points="2"] {
    background: #f1f1cf; 
    }
.filter input:checked + span[data-points="3"] {
    background: #edc894; 
    }
.filter input:checked + span[data-points="4"] {
    background: #ea967c; 
    }
.filter input:checked + span[data-points="5"] {
    background: #a6181a; 
    opacity: 0.6;
    }

/* .ivu-checkbox {
    display: none !important;
} */

/* .ivu-checkbox+span, .ivu-checkbox-wrapper+span{
    margin-right: 0px !important; 
}

.ivu-checkbox-wrapper-checked.ivu-checkbox-border {
    border-color: #f1f1f1 !important;
} */

.ivu-input {
    display: inline-block;
    width: 100%;
    height: 32px;
    line-height: 1.5;
    /* padding: 4px 17px !important; */
    font-size: 14px;
    /* border: none !important; */
    /* border-radius: 0px !important; */
    color: #515a6e;
    background-color: #fff;
    background-image: none;
    position: relative;
    cursor: text;
    transition: border .2s ease-in-out,background .2sD4D6E0 ease-in-out,box-shadow .2s ease-in-out;
    /* border-bottom: 1.2px solid #D4D6E0 !important; */
}

.ivu-input:focus {
    border-color: #f1f1f1 !important;
    outline: 0;
    box-shadow: none !important;
}

.ivu-input:hover {
    border-color: #f1f1f1 !important;
}

/* .ivu-checkbox-border {
    border: 1px solid #dcdee2;
    border-radius: 4px;
    height: 28px !important;
    line-height: 28px !important;
    padding: 0 8px !important;
    transition: border .2s ease-in-out;
} */

.similar {
    /* background-color: #F6F4F9; */
    /* border-radius: 20px; */
    /* width: 180px; */
    margin-right: 20px;
    margin-bottom: 20px;
}
  
.add {
    background-color: rgb(246, 244, 249);
    border: none;
    border-radius: 5px;
    padding: 6px 12px;
    color: rgb(120, 137, 179);
    margin-top: 6px;
    font-weight: bolder;
}

.add:active {  
    outline: none; 
    background-color: #333333;  
}

.add:focus {  
    outline: none; 
}

.away {
    background-color: #D4D6E0;
    border: none;
    border-radius: 5px;
    padding: 6px 12px;
    color: #fff;
    margin-top: 6px;
    font-weight: bolder;
}

.away:active {  
    outline: none; 
    background-color: #D4D6E0;  
}

.away:focus {  
    outline: none; 
}

.ivu-list-container{
    border: #fff !important;
}

.ivu-auto-complete.ivu-select-dropdown {
    max-height: 300px !important;
}

/* input:checked ~ label[for="slide1"],
input:checked ~ label[for="slide2"],
input:checked ~ label[for="slide3"],
input:checked ~ label[for="slide4"] {
  background: #333;
} */

.ivu-select-visible .ivu-select-selection {
    border-color: #DBDDE1 !important;
    outline: 0;
    box-shadow: 0 0 0 0 !important;
}

.ivu-select-selection-focused, .ivu-select-selection:hover {
    border-color: #DBDDE1 !important;
}


.ivu-slider-bar {
    height: 4px;
    /* background: #57a3f3; */
    background: #979797 !important;
    border-radius: 3px;
    position: absolute;
}

.ivu-slider-button {
    width: 12px;
    height: 12px;
    border: 2px solid #979797 !important;
    border-radius: 50%;
    background-color: #fff;
    transition: all .2s linear;
    outline: 0;
}

.ivu-slider-button-dragging, .ivu-slider-button:focus, .ivu-slider-button:hover {
    /* border-color: #2d8cf0; */
    border-color: #979797 !important;
    transform: scale(1.5);
}

.ivu-switch-checked {
    border-color: #979797 !important;
    background-color: #979797 !important;
}


li.ingredient:hover{
    cursor: pointer;
    color:rgb(120, 137, 179);
}

.similar div:hover .product{
    cursor: pointer;
    color:rgb(120, 137, 179);
}

#ing ul li{
    min-height: 35px;
    padding: 3px 0px;
}

#pro div p#productname:hover{
    cursor: pointer;
    color:rgb(120, 137, 179);
}

/* input[type="checkbox"], input[type="radio"] {
  display: none;
}
label input[type="checkbox"] ~ span{
  display: inline-block;
  width: 12px;
  height: 12px;
  vertical-align: top;
  border: 2px solid #999;
  border-radius:100%;
  box-sizing: content-box;
  -moz-box-sizing: content-box;
  margin-top: 3px;
} */
/* label input[type="checkbox"] ~ span {
  border-radius: 2px;
} */

/* label input[type="checkbox"]:checked ~ span{
  background-color: #000;
}
label:hover input[type="checkbox"] ~ span{
  border-color: #666;
} */


.switch input { 
    display:none;
}
.switch {
    display:inline-block;
    width:50px;
    height:18px;
    /* margin:8px; */
    transform:translateY(50%);
    position:relative;
}
/* Style Wired */
.slider {
    position:absolute;
    top:0;
    bottom:0;
    left:0;
    right:0;
    border-radius:30px;
    box-shadow:0 0 0 2px #979797, 0 0 2px #979797;
    cursor:pointer;
    border:4px solid transparent;
    overflow:hidden;
     transition:.4s;
}
.slider:before {
    position:absolute;
    content:"";
    width:100%;
    height:100%;
    background:#979797;
    border-radius:30px;
    transform:translateX(-30px);
    transition:.4s;
}

input:checked + .slider:before {
    transform:translateX(30px);
    background:#7886B5;
}
input:checked + .slider {
    box-shadow:0 0 0 2px #7886B5,0 0 2px #7886B5;
}

/* Style Flat */
.switch.flat .slider {
 box-shadow:none;
}
.switch.flat .slider:before {
  background:#FFF;
}
.switch.flat input:checked + .slider:before {
 background:white;
}
.switch.flat input:checked + .slider {
  background:#7886B5;
}


</style>